import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';

const GameBalanceOptimizer = () => {
  const [params, setParams] = useState({
    // Player stats by level
    playerATK: [3, 4, 5],
    playerDEF: [0.75, 1.5, 2],
    playerRevenge: [0.2, 0.4, 0.6],
    playerHP: [10, 8, 6],  // HP inversely related to DEF
    
    // Monster stats by level
    monsterATK: [3, 5, 7],
    monsterDEF: [1.5, 3, 4],
    monsterRevenge: [0.2, 0.4, 0.6],
    monsterHP: [5, 6, 7],
    
    battleTurns: [5, 6, 7]
  });

  const strategies = [
    { name: 'Offense', atkLv: 3, defLv: 1 },
    { name: 'Balanced', atkLv: 2, defLv: 2 },
    { name: 'Tank', atkLv: 1, defLv: 3 }
  ];

  const updateParam = (category, index, value) => {
    setParams(prev => ({
      ...prev,
      [category]: prev[category].map((v, i) => i === index ? parseFloat(value) : v)
    }));
  };

  // Calculate PvP damage
  const calcPvPDamage = (atkLv, defLv1, defLv2) => {
    const atk = params.playerATK[atkLv - 1];
    const def = params.playerDEF[defLv2 - 1];
    const rev = params.playerRevenge[defLv1 - 1];
    return atk - def + rev;
  };

  // Calculate PvP outcome considering HP (returns turns to kill)
  const calcPvPOutcome = (atkLv1, defLv1, atkLv2, defLv2) => {
    const dmg1to2 = calcPvPDamage(atkLv1, defLv1, defLv2);
    const dmg2to1 = calcPvPDamage(atkLv2, defLv2, defLv1);
    
    const hp1 = params.playerHP[defLv1 - 1];
    const hp2 = params.playerHP[defLv2 - 1];
    
    const turnsFor1ToKill2 = dmg1to2 > 0 ? hp2 / dmg1to2 : Infinity;
    const turnsFor2ToKill1 = dmg2to1 > 0 ? hp1 / dmg2to1 : Infinity;
    
    return {
      dmg1to2,
      dmg2to1,
      hp1,
      hp2,
      turnsFor1ToKill2,
      turnsFor2ToKill1,
      player1Wins: turnsFor1ToKill2 < turnsFor2ToKill1
    };
  };

  // Calculate PvE damage (per player to monster)
  const calcPvEDamageToMonster = (playerAtkLv, monsterDefLv, playerDefLv) => {
    const atk = params.playerATK[playerAtkLv - 1];
    const def = params.monsterDEF[monsterDefLv - 1];
    const rev = params.playerRevenge[playerDefLv - 1];
    return atk - def + rev / 2;
  };

  // Calculate PvE damage (from monster to player)
  const calcPvEDamageToPlayer = (monsterAtkLv, playerDefLv, monsterDefLv) => {
    const atk = params.monsterATK[monsterAtkLv - 1];
    const def = params.playerDEF[playerDefLv - 1];
    const rev = params.monsterRevenge[monsterDefLv - 1];
    return (atk - def) / 2 + rev;
  };

  // Calculate turns to win for PvE
  const calcTurnsToWin = (playerAtkLv, playerDefLv, monsterAtkLv, monsterDefLv) => {
    const dmgToMonster = calcPvEDamageToMonster(playerAtkLv, monsterDefLv, playerDefLv) * 2; // 2 players
    const dmgToPlayer = calcPvEDamageToPlayer(monsterAtkLv, playerDefLv, monsterDefLv);
    
    const monsterHP = params.monsterHP[Math.max(monsterAtkLv, monsterDefLv) - 1];
    const playerHP = params.playerHP[Math.max(playerAtkLv, playerDefLv) - 1];
    
    const turnsToKillMonster = dmgToMonster > 0 ? monsterHP / dmgToMonster : Infinity;
    const turnsToKillPlayer = dmgToPlayer > 0 ? playerHP / dmgToPlayer : Infinity;
    
    return {
      turnsToKillMonster,
      turnsToKillPlayer,
      playerWins: turnsToKillMonster < turnsToKillPlayer,
      dmgToMonster,
      dmgToPlayer
    };
  };

  // Generate PvP matchup matrix
  const generatePvPMatrix = () => {
    const matrix = [];
    strategies.forEach(s1 => {
      strategies.forEach(s2 => {
        const dmg = calcPvPDamage(s1.atkLv, s1.defLv, s2.defLv);
        matrix.push({
          attacker: s1.name,
          defender: s2.name,
          damage: dmg.toFixed(2)
        });
      });
    });
    return matrix;
  };

  // Generate PvE analysis
  const generatePvEAnalysis = () => {
    const results = [];
    const monsterLevels = [
      { name: 'Easy (1-1)', atkLv: 1, defLv: 1 },
      { name: 'Medium (2-2)', atkLv: 2, defLv: 2 },
      { name: 'Hard (3-3)', atkLv: 3, defLv: 3 },
      { name: 'Glass Cannon (3-1)', atkLv: 3, defLv: 1 },
      { name: 'Tank Boss (1-3)', atkLv: 1, defLv: 3 }
    ];

    strategies.forEach(strat => {
      monsterLevels.forEach(monster => {
        const result = calcTurnsToWin(strat.atkLv, strat.defLv, monster.atkLv, monster.defLv);
        results.push({
          strategy: strat.name,
          monster: monster.name,
          turnsToWin: result.turnsToKillMonster.toFixed(1),
          turnsToLose: result.turnsToKillPlayer.toFixed(1),
          winMargin: (result.turnsToKillPlayer - result.turnsToKillMonster).toFixed(1),
          outcome: result.playerWins ? 'WIN' : 'LOSE'
        });
      });
    });
    return results;
  };

  // Check circular relationship
  const checkCircularRelationship = () => {
    const offVsTank = calcPvPOutcome(3, 1, 1, 3);
    const tankVsBal = calcPvPOutcome(1, 3, 2, 2);
    const balVsOff = calcPvPOutcome(2, 2, 3, 1);

    return {
      offVsTank: { 
        offDmg: offVsTank.dmg1to2.toFixed(2), 
        tankDmg: offVsTank.dmg2to1.toFixed(2),
        offHP: offVsTank.hp1,
        tankHP: offVsTank.hp2,
        offTurns: offVsTank.turnsFor1ToKill2.toFixed(2),
        tankTurns: offVsTank.turnsFor2ToKill1.toFixed(2),
        diff: (offVsTank.turnsFor2ToKill1 - offVsTank.turnsFor1ToKill2).toFixed(2),
        stronger: offVsTank.player1Wins
      },
      tankVsBal: { 
        tankDmg: tankVsBal.dmg1to2.toFixed(2),
        balDmg: tankVsBal.dmg2to1.toFixed(2),
        tankHP: tankVsBal.hp1,
        balHP: tankVsBal.hp2,
        tankTurns: tankVsBal.turnsFor1ToKill2.toFixed(2),
        balTurns: tankVsBal.turnsFor2ToKill1.toFixed(2),
        diff: (tankVsBal.turnsFor2ToKill1 - tankVsBal.turnsFor1ToKill2).toFixed(2),
        stronger: tankVsBal.player1Wins
      },
      balVsOff: { 
        balDmg: balVsOff.dmg1to2.toFixed(2),
        offDmg: balVsOff.dmg2to1.toFixed(2),
        balHP: balVsOff.hp1,
        offHP: balVsOff.hp2,
        balTurns: balVsOff.turnsFor1ToKill2.toFixed(2),
        offTurns: balVsOff.turnsFor2ToKill1.toFixed(2),
        diff: (balVsOff.turnsFor2ToKill1 - balVsOff.turnsFor1ToKill2).toFixed(2),
        stronger: balVsOff.player1Wins
      }
    };
  };

  const pvpMatrix = generatePvPMatrix();
  const pveAnalysis = generatePvEAnalysis();
  const circularCheck = checkCircularRelationship();

  return (
    <div className="w-full max-w-6xl mx-auto p-6 bg-gray-50">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Card Game Balance Optimizer</h1>
      
      {/* Parameter Input Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Parameters</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Player Stats */}
          <div>
            <h3 className="font-semibold mb-3 text-gray-600">Player Stats (by Level)</h3>
            {['ATK', 'DEF', 'Revenge', 'HP'].map(stat => (
              <div key={stat} className="mb-3">
                <label className="block text-sm font-medium text-gray-600 mb-1">{stat}</label>
                <div className="flex gap-2">
                  {[0, 1, 2].map(i => (
                    <input
                      key={i}
                      type="number"
                      step="0.1"
                      value={params[`player${stat}`][i]}
                      onChange={(e) => updateParam(`player${stat}`, i, e.target.value)}
                      className="w-20 px-2 py-1 border rounded text-sm"
                      placeholder={`Lv${i+1}`}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Monster Stats */}
          <div>
            <h3 className="font-semibold mb-3 text-gray-600">Monster Stats (by Level)</h3>
            {['ATK', 'DEF', 'Revenge', 'HP'].map(stat => (
              <div key={stat} className="mb-3">
                <label className="block text-sm font-medium text-gray-600 mb-1">{stat}</label>
                <div className="flex gap-2">
                  {[0, 1, 2].map(i => (
                    <input
                      key={i}
                      type="number"
                      step="0.1"
                      value={params[`monster${stat}`][i]}
                      onChange={(e) => updateParam(`monster${stat}`, i, e.target.value)}
                      className="w-20 px-2 py-1 border rounded text-sm"
                      placeholder={`Lv${i+1}`}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Circular Relationship Check */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Circular Relationship Check (with HP)</h2>
        <div className="grid grid-cols-3 gap-4">
          <div className={`p-4 rounded ${circularCheck.offVsTank.stronger ? 'bg-green-100' : 'bg-red-100'}`}>
            <div className="font-semibold">Offense vs Tank</div>
            <div className="text-2xl font-bold my-2">{circularCheck.offVsTank.diff > 0 ? '+' : ''}{circularCheck.offVsTank.diff} turns</div>
            <div className="text-xs text-gray-600 space-y-1">
              <div>Off: {circularCheck.offVsTank.offDmg} dmg/turn × {circularCheck.offVsTank.tankHP} HP = {circularCheck.offVsTank.offTurns} turns</div>
              <div>Tank: {circularCheck.offVsTank.tankDmg} dmg/turn × {circularCheck.offVsTank.offHP} HP = {circularCheck.offVsTank.tankTurns} turns</div>
            </div>
            <div className="text-sm font-semibold mt-2">{circularCheck.offVsTank.stronger ? '✓ Offense wins' : '✗ Tank wins'}</div>
          </div>
          <div className={`p-4 rounded ${circularCheck.tankVsBal.stronger ? 'bg-green-100' : 'bg-red-100'}`}>
            <div className="font-semibold">Tank vs Balanced</div>
            <div className="text-2xl font-bold my-2">{circularCheck.tankVsBal.diff > 0 ? '+' : ''}{circularCheck.tankVsBal.diff} turns</div>
            <div className="text-xs text-gray-600 space-y-1">
              <div>Tank: {circularCheck.tankVsBal.tankDmg} dmg/turn × {circularCheck.tankVsBal.balHP} HP = {circularCheck.tankVsBal.tankTurns} turns</div>
              <div>Bal: {circularCheck.tankVsBal.balDmg} dmg/turn × {circularCheck.tankVsBal.tankHP} HP = {circularCheck.tankVsBal.balTurns} turns</div>
            </div>
            <div className="text-sm font-semibold mt-2">{circularCheck.tankVsBal.stronger ? '✓ Tank wins' : '✗ Balanced wins'}</div>
          </div>
          <div className={`p-4 rounded ${circularCheck.balVsOff.stronger ? 'bg-green-100' : 'bg-red-100'}`}>
            <div className="font-semibold">Balanced vs Offense</div>
            <div className="text-2xl font-bold my-2">{circularCheck.balVsOff.diff > 0 ? '+' : ''}{circularCheck.balVsOff.diff} turns</div>
            <div className="text-xs text-gray-600 space-y-1">
              <div>Bal: {circularCheck.balVsOff.balDmg} dmg/turn × {circularCheck.balVsOff.offHP} HP = {circularCheck.balVsOff.balTurns} turns</div>
              <div>Off: {circularCheck.balVsOff.offDmg} dmg/turn × {circularCheck.balVsOff.balHP} HP = {circularCheck.balVsOff.offTurns} turns</div>
            </div>
            <div className="text-sm font-semibold mt-2">{circularCheck.balVsOff.stronger ? '✓ Balanced wins' : '✗ Offense wins'}</div>
          </div>
        </div>
      </div>

      {/* PvP Damage Matrix */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">PvP Outcome Matrix (with HP)</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full border-collapse">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2">Attacker →<br/>Defender ↓</th>
                <th className="border p-2">Offense<br/>(HP: {params.playerHP[0]})</th>
                <th className="border p-2">Balanced<br/>(HP: {params.playerHP[1]})</th>
                <th className="border p-2">Tank<br/>(HP: {params.playerHP[2]})</th>
              </tr>
            </thead>
            <tbody>
              {strategies.map(defender => (
                <tr key={defender.name}>
                  <td className="border p-2 font-semibold bg-gray-50">
                    {defender.name}<br/>
                    <span className="text-xs text-gray-600">(HP: {params.playerHP[defender.defLv - 1]})</span>
                  </td>
                  {strategies.map(attacker => {
                    if (attacker.name === defender.name) {
                      return (
                        <td key={attacker.name} className="border p-2 text-center bg-gray-100">
                          <div className="text-gray-400">-</div>
                        </td>
                      );
                    }
                    const outcome = calcPvPOutcome(attacker.atkLv, attacker.defLv, defender.atkLv, defender.defLv);
                    const bgColor = outcome.player1Wins ? 'bg-green-100' : 'bg-red-100';
                    return (
                      <td key={attacker.name} className={`border p-2 text-center ${bgColor}`}>
                        <div className="font-bold text-lg">{outcome.turnsFor1ToKill2.toFixed(1)} turns</div>
                        <div className="text-xs text-gray-600">{outcome.dmg1to2.toFixed(1)} dmg/turn</div>
                        <div className="text-xs font-semibold mt-1">
                          {outcome.player1Wins ? '✓ WIN' : '✗ LOSE'}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-3 text-sm text-gray-600">
          <div>• Green = Row player (attacker) wins by killing column player first</div>
          <div>• Red = Column player wins</div>
          <div>• Number shows turns needed for row player to kill column player</div>
        </div>
      </div>

      {/* PvE Analysis */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">PvE Balance Analysis</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full border-collapse text-sm">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2">Strategy</th>
                <th className="border p-2">Monster Type</th>
                <th className="border p-2">Turns to Win</th>
                <th className="border p-2">Turns to Lose</th>
                <th className="border p-2">Win Margin</th>
                <th className="border p-2">Outcome</th>
              </tr>
            </thead>
            <tbody>
              {pveAnalysis.map((row, idx) => (
                <tr key={idx} className={row.outcome === 'WIN' ? 'bg-green-50' : 'bg-red-50'}>
                  <td className="border p-2">{row.strategy}</td>
                  <td className="border p-2">{row.monster}</td>
                  <td className="border p-2 text-center">{row.turnsToWin}</td>
                  <td className="border p-2 text-center">{row.turnsToLose}</td>
                  <td className="border p-2 text-center">{row.winMargin}</td>
                  <td className="border p-2 text-center font-semibold">{row.outcome}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Design Notes */}
      <div className="bg-blue-50 rounded-lg p-6 mt-6">
        <h3 className="font-semibold text-blue-900 mb-2">Mathematical Constraint Check</h3>
        <div className="text-sm text-blue-800 mb-3">
          For the circular relationship to be possible, this must be negative:
          <div className="font-mono bg-blue-100 p-2 mt-1 rounded">
            H₃(D₂ - D₁) + H₂(D₁ - D₃) + H₁(D₃ - D₂) = {
              (() => {
                const h1 = params.playerHP[0];
                const h2 = params.playerHP[1];
                const h3 = params.playerHP[2];
                const d1 = params.playerDEF[0];
                const d2 = params.playerDEF[1];
                const d3 = params.playerDEF[2];
                const value = h3 * (d2 - d1) + h2 * (d1 - d3) + h1 * (d3 - d2);
                return (
                  <span className={value < 0 ? 'text-green-700 font-bold' : 'text-red-700 font-bold'}>
                    {value.toFixed(3)} {value < 0 ? '✓ (Solvable!)' : '✗ (Not solvable)'}
                  </span>
                );
              })()
            }
          </div>
        </div>
        <h3 className="font-semibold text-blue-900 mb-2 mt-4">Design Guidelines</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Green boxes indicate the circular relationship is working correctly</li>
          <li>• The difference shown is in turns (positive = winner has time to spare)</li>
          <li>• HP inversely proportional to DEF helps achieve balance (glass cannon vs tank)</li>
          <li>• Aim for similar turn margins (±0.5-1.5 turns) across all three matchups</li>
          <li>• Revenge values should increase with DEF level for proper balance</li>
        </ul>
      </div>
    </div>
  );
};

export default GameBalanceOptimizer;
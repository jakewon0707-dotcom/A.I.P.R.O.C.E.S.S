"use client";
import React, { useEffect } from "react";
import confetti from "canvas-confetti";

interface Props {
  score: number | null;
  targetSentence: string;
  spokenText: string;
}

export default function ResultBoard({ score, targetSentence, spokenText }: Props) {
  useEffect(() => {
    if (score !== null && score >= 90) {
      // Trigger confetti
      const duration = 3 * 1000;
      const end = Date.now() + duration;

      const frame = () => {
        confetti({
          particleCount: 8,
          angle: 60,
          spread: 55,
          origin: { x: 0 },
          colors: ['#34D399', '#FBBF24', '#F87171', '#60A5FA', '#A78BFA']
        });
        confetti({
          particleCount: 8,
          angle: 120,
          spread: 55,
          origin: { x: 1 },
          colors: ['#34D399', '#FBBF24', '#F87171', '#60A5FA', '#A78BFA']
        });

        if (Date.now() < end) {
          requestAnimationFrame(frame);
        }
      };
      frame();
    }
  }, [score]);

  if (score === null) return null;

  // Simple diff highlighting
  const cleanTarget = targetSentence.toLowerCase().replace(/[.,!?]/g, '').split(' ');
  const cleanSpoken = spokenText.toLowerCase().replace(/[.,!?]/g, '').split(' ');
  const spokenSet = new Set(cleanSpoken);

  return (
    <div className="w-full bg-white p-8 md:p-12 rounded-[2.5rem] cool-shadow border-[3px] border-slate-50 mt-12 animate-in fade-in slide-in-from-bottom-8 duration-500">
      <h3 className="text-3xl font-black text-center text-slate-700 mb-8 bg-slate-100 inline-block px-8 py-3 rounded-full mx-auto flex w-max">📊 AI 분석 결과</h3>
      
      <div className="mb-10">
        <div className="flex justify-between items-end mb-4">
          <span className="text-2xl font-bold text-slate-500">유사도 (Similarity)</span>
          <span className={`text-5xl font-black ${score >= 80 ? 'text-emerald-500' : 'text-rose-500'}`}>
            {score}%
          </span>
        </div>
        
        {/* Progress Bar Background */}
        <div className="w-full h-8 bg-slate-100 rounded-full overflow-hidden cool-shadow shadow-inner">
          {/* Progress Bar Fill */}
          <div 
            className={`h-full transition-all duration-1000 ease-out rounded-full ${score >= 90 ? 'bg-gradient-to-r from-emerald-400 to-emerald-300' : score >= 70 ? 'bg-gradient-to-r from-amber-400 to-amber-300' : 'bg-gradient-to-r from-rose-400 to-rose-300'}`}
            style={{ width: `${score}%` }}
          />
        </div>
      </div>

      <div className="bg-slate-50 p-8 rounded-[2rem] border-[3px] border-slate-100 mb-10">
        <p className="text-slate-400 font-bold mb-3 text-lg">🗣️ 내가 한 말:</p>
        <p className="text-3xl text-slate-700 font-bold mb-8 bg-white p-6 rounded-2xl cool-shadow block">{spokenText || "(소리가 인식되지 않았어요)"}</p>
        
        <p className="text-slate-400 font-bold mb-4 text-lg">🔎 AI 피드백 (단어 매칭):</p>
        <div className="flex flex-wrap gap-3 text-3xl">
          {cleanTarget.map((word, idx) => (
            <span 
              key={idx} 
              className={`px-4 py-2 rounded-2xl font-black border-[3px] ${
                spokenSet.has(word) 
                  ? 'bg-emerald-100 text-emerald-600 border-emerald-200' 
                  : 'bg-rose-100 text-rose-500 border-rose-200 line-through opacity-80'
              }`}
            >
              {word}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-8 text-center pb-4">
        {score >= 90 ? (
          <div className="text-5xl font-black text-emerald-500 animate-bounce drop-shadow-sm">
            🎉 Perfect! You beat the teacher! 🏆
          </div>
        ) : score >= 70 ? (
          <div className="text-3xl font-bold text-amber-500">
            👍 Good job! 거의 다왔어요! 한 번 더 도전? 😉
          </div>
        ) : (
          <div className="text-3xl font-bold text-rose-500">
            💪 Keep trying! 포기하지 말고 다시 한 번 해볼까요!
          </div>
        )}
      </div>
    </div>
  );
}

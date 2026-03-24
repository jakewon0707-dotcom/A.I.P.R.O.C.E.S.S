"use client";
import React from "react";
import { Mic, Square } from "lucide-react";

interface Props {
  isRecording: boolean;
  onToggleRecord: () => void;
}

export default function JellyButton({ isRecording, onToggleRecord }: Props) {
  return (
    <div className="flex flex-col items-center justify-center py-6 w-full">
      <div className="bg-rose-100 text-rose-500 px-6 py-2 rounded-full font-black text-xl mb-10">
        🎙️ [2단계] 나의 도전!
      </div>

      <div className="relative">
        {/* Animated expanding ring when recording */}
        {isRecording && (
           <div className="absolute inset-0 bg-rose-400 rounded-[3rem] animate-ping opacity-60"></div>
        )}
        <button 
          onClick={onToggleRecord}
          className={`relative z-10 flex flex-col items-center justify-center gap-3 w-56 h-56 rounded-[3rem] transition-all duration-200
            ${isRecording 
              ? 'bg-rose-500 text-white jelly-active rotate-2 scale-95' 
              : 'bg-rose-400 text-white jelly-shadow active:jelly-active hover:-translate-y-2 hover:bg-rose-300'
            }
          `}
        >
          <div className="bg-white/20 p-4 rounded-full">
            {isRecording ? <Square size={48} fill="currentColor" /> : <Mic size={64} />}
          </div>
          <span className="text-3xl font-black tracking-wide">
            {isRecording ? "녹음 종료" : "도전하기!"}
          </span>
        </button>
      </div>
      
      <div className="mt-12 h-8">
        <p className={`font-bold text-2xl transition-all ${isRecording ? 'text-rose-500 animate-pulse' : 'text-slate-400'}`}>
          {isRecording ? "AI가 조용히 듣고 있어요... ✨" : "버튼을 누르고 자신 있게 말해봐!"}
        </p>
      </div>
    </div>
  );
}

"use client";
import React from "react";
import { Headphones } from "lucide-react";

interface Props {
  countryOptions: string[];
  selectedCountry: string;
  onSelectCountry: (c: string) => void;
  targetSentence: string;
}

export default function MissionCard({ countryOptions, selectedCountry, onSelectCountry, targetSentence }: Props) {
  const handleListen = () => {
    const utterance = new SpeechSynthesisUtterance(targetSentence);
    utterance.lang = "en-US";
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="bg-white p-6 md:p-10 rounded-3xl cool-shadow border-2 border-slate-50 flex flex-col items-center w-full">
      <div className="bg-sky-100 text-sky-600 px-6 py-2 rounded-full font-black text-xl mb-6">
        👨‍🏫 [1단계] 선생님 미션
      </div>
      
      <div className="w-full max-w-sm mb-6">
        <label className="text-slate-400 text-sm font-bold mb-2 block text-center">🌏 출신 국가를 선택하세요</label>
        <select 
          className="w-full p-4 rounded-2xl bg-slate-50 border-2 border-sky-100 text-slate-700 text-xl font-bold outline-none focus:border-sky-300 text-center transition-colors appearance-none cursor-pointer"
          value={selectedCountry}
          onChange={(e) => onSelectCountry(e.target.value)}
        >
          {countryOptions.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      <div className="w-full bg-gradient-to-r from-sky-50 to-blue-50 py-10 px-4 rounded-[2rem] border-4 border-dashed border-sky-200 text-center mb-8 relative transition-all hover:scale-105">
        <span className="text-sky-600 text-4xl md:text-5xl font-black drop-shadow-sm">{`"${targetSentence}"`}</span>
      </div>

      <button 
        onClick={handleListen}
        className="flex items-center gap-3 bg-sky-500 hover:bg-sky-400 text-white font-bold text-2xl px-10 py-5 rounded-full jelly-shadow active:jelly-active transition-all"
      >
        <Headphones size={28} />
        선생님 발음 듣기
      </button>
    </div>
  );
}

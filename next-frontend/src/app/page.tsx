"use client";
import React, { useState, useEffect, useRef } from "react";
import MissionCard from "@/components/MissionCard";
import JellyButton from "@/components/JellyButton";
import ResultBoard from "@/components/ResultBoard";
import { compareTwoStrings } from "string-similarity"; 

const LESSON_1_COUNTRIES = ["the USA", "the UK", "Korea", "Canada", "Australia", "Vietnam"];

export default function App() {
  const [selectedCountry, setSelectedCountry] = useState(LESSON_1_COUNTRIES[2]);
  const [targetSentence, setTargetSentence] = useState(`I'm from ${LESSON_1_COUNTRIES[2]}.`);
  const [isRecording, setIsRecording] = useState(false);
  const [spokenText, setSpokenText] = useState("");
  const [score, setScore] = useState<number | null>(null);

  // Web Speech API Ref
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    setTargetSentence(`I'm from ${selectedCountry}.`);
    setScore(null);
    setSpokenText("");
  }, [selectedCountry]);

  useEffect(() => {
    // Initialize SpeechRecognition on the Client
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setSpokenText(transcript);
        
        const cleanTarget = targetSentence.toLowerCase().replace(/[.,!?]/g, '').trim();
        const cleanSpoken = transcript.toLowerCase().replace(/[.,!?]/g, '').trim();
        
        const simScore = Math.round(compareTwoStrings(cleanTarget, cleanSpoken) * 100);
        setScore(simScore);
        setIsRecording(false);
      };

      recognition.onerror = (event: any) => {
        console.error("Speech recognition error:", event.error);
        if (event.error !== 'no-speech') {
           setSpokenText(`(에러 발생: ${event.error}. 마이크 권한을 허용했는지 확인해주세요.)`);
        }
        setIsRecording(false);
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current = recognition;
    } else {
      console.warn("Speech Recognition API is not supported in this browser.");
    }
  }, [targetSentence]);

  const handleToggleRecord = () => {
    if (!recognitionRef.current) {
      alert("크롬(Chrome)이나 엣지(Edge) 브라우저에서 마이크 기능을 지원합니다!");
      return;
    }

    if (isRecording) {
      recognitionRef.current.stop();
      setIsRecording(false);
    } else {
      setScore(null);
      setSpokenText("");
      setIsRecording(true);
      try {
        recognitionRef.current.start();
      } catch (e) {
        console.error("Microphone access issue:", e);
      }
    }
  };

  return (
    <main className="min-h-screen pt-12 pb-24 px-4 md:px-8 max-w-5xl mx-auto flex flex-col items-center">
      
      {/* Header */}
      <header className="text-center mb-16 w-full fade-in-up">
        <div className="inline-block bg-white px-10 py-4 rounded-full cool-shadow border-[3px] border-slate-50 mb-6 transition-transform hover:scale-105 cursor-default">
          <h1 className="text-4xl md:text-6xl font-black text-sky-500 tracking-tight">
            🌟 A.I. P.R.O.C.E.S.S. Tutor
          </h1>
        </div>
        <p className="text-2xl md:text-3xl text-rose-400 font-bold max-w-2xl mx-auto leading-relaxed">
          "선생님의 발음을 완벽하게 따라잡고<br className="hidden md:block" /> 펑퍼짐한 풍선을 터뜨려봐!"
        </p>
      </header>

      {/* Main Content Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 w-full">
        {/* Left Column: Teacher Mission */}
        <MissionCard 
          countryOptions={LESSON_1_COUNTRIES}
          selectedCountry={selectedCountry}
          onSelectCountry={setSelectedCountry}
          targetSentence={targetSentence}
        />
        
        {/* Right Column: Student Submission */}
        <div className="flex flex-col items-center justify-center bg-white rounded-3xl cool-shadow border-2 border-slate-50 p-6 md:p-10 w-full h-full">
          <JellyButton 
            isRecording={isRecording}
            onToggleRecord={handleToggleRecord}
          />
        </div>
      </div>

      {/* Results */}
      {score !== null && (
        <ResultBoard 
          score={score}
          targetSentence={targetSentence}
          spokenText={spokenText}
        />
      )}

    </main>
  );
}

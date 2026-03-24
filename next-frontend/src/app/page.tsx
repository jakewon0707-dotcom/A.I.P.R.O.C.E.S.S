"use client";
import React, { useState, useEffect, useRef } from "react";
import MissionCard from "@/components/MissionCard";
import JellyButton from "@/components/JellyButton";
import ResultBoard from "@/components/ResultBoard";
import { compareTwoStrings } from "string-similarity"; 
import { supabase } from "@/lib/supabase";

const LESSON_GRADES = ["1st", "2nd", "3rd", "4th", "5th", "6th"];

export default function App() {
  const [selectedGrade, setSelectedGrade] = useState(LESSON_GRADES[5]);
  const [targetSentence, setTargetSentence] = useState(`I'm in ${LESSON_GRADES[5]} grade.`);
  const [studentId, setStudentId] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [spokenText, setSpokenText] = useState("");
  const [score, setScore] = useState<number | null>(null);

  // Web Speech API Ref
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    setTargetSentence(`I'm in ${selectedGrade} grade.`);
    setScore(null);
    setSpokenText("");
  }, [selectedGrade]);

  useEffect(() => {
    // Initialize SpeechRecognition on the Client
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";

      recognition.onresult = async (event: any) => {
        const transcript = event.results[0][0].transcript;
        setSpokenText(transcript);
        
        const cleanTarget = targetSentence.toLowerCase().replace(/[.,!?]/g, '').trim();
        const cleanSpoken = transcript.toLowerCase().replace(/[.,!?]/g, '').trim();
        
        const simScore = Math.round(compareTwoStrings(cleanTarget, cleanSpoken) * 100);
        setScore(simScore);
        setIsRecording(false);

        if (studentId) {
          try {
            await supabase.from("student_scores").insert([{
              student_id: studentId,
              sentence: targetSentence,
              score: simScore
            }]);
          } catch (err) {
            console.error("Failed to save score:", err);
          }
        }
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
    if (!studentId.trim()) {
      alert("먼저 이름이나 번호를 입력해주세요! (예: 6학년 1반 1번 -> 60101)");
      return;
    }

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

        {/* Student ID Input */}
        <div className="mt-8 bg-white p-6 rounded-3xl cool-shadow border-2 border-slate-50 max-w-sm mx-auto">
          <label className="text-slate-500 text-sm font-bold mb-3 block">🧑‍🎓 이름 또는 학번을 입력하세요</label>
          <input 
            type="text" 
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            placeholder="예: 홍길동 또는 60101"
            className="w-full p-4 rounded-2xl bg-slate-50 border-2 border-sky-100 text-slate-700 text-xl font-bold outline-none focus:border-sky-300 text-center transition-colors"
          />
        </div>
      </header>

      {/* Main Content Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 w-full">
        {/* Left Column: Teacher Mission */}
        <MissionCard 
          gradeOptions={LESSON_GRADES}
          selectedGrade={selectedGrade}
          onSelectGrade={setSelectedGrade}
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

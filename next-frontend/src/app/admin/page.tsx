"use client";
import React, { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function AdminDashboard() {
  const [records, setRecords] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    setLoading(true);
    const { data, error } = await supabase
      .from("student_scores")
      .select("*")
      .order("created_at", { ascending: false });

    if (error) {
      console.error("Error fetching records:", error);
    } else {
      setRecords(data || []);
    }
    setLoading(false);
  };

  const handleDownloadCSV = () => {
    if (records.length === 0) return;

    // Build CSV content
    const headers = ["ID", "학생 명/학번", "연습 문장", "점수", "녹음 일시"];
    const csvRows = [headers.join(",")];

    records.forEach(record => {
      const dateStr = new Date(record.created_at).toLocaleString('ko-KR');
      const row = [
        record.id,
        `"${record.student_id}"`, // Handle commas in name
        `"${record.sentence}"`,
        record.score,
        `"${dateStr}"`
      ];
      csvRows.push(row.join(","));
    });

    // Create Blob and trigger download
    const csvString = csvRows.join("\n");
    const blob = new Blob(["\uFEFF" + csvString], { type: "text/csv;charset=utf-8;" }); // UTF-8 BOM for Excel
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `student_scores_${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <main className="min-h-screen bg-slate-50 p-8">
      <div className="max-w-6xl mx-auto bg-white rounded-3xl p-8 md:p-12 cool-shadow border-2 border-slate-100">
        <header className="flex flex-col md:flex-row justify-between items-center mb-10 gap-4">
          <h1 className="text-3xl font-black text-sky-600">📊 학생 학습 관리 시스템 (Admin)</h1>
          <div className="flex gap-4">
            <button 
              onClick={fetchRecords} 
              className="px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-600 font-bold rounded-xl transition-colors"
            >
              새로고침
            </button>
            <button 
              onClick={handleDownloadCSV} 
              disabled={records.length === 0}
              className="px-6 py-3 bg-rose-500 hover:bg-rose-400 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              엑셀(CSV) 다운로드
            </button>
          </div>
        </header>

        {loading ? (
          <div className="text-center text-slate-400 py-20 font-bold text-xl">데이터를 불러오는 중입니다...</div>
        ) : records.length === 0 ? (
          <div className="text-center text-slate-400 py-20 font-bold text-xl">저장된 기록이 없습니다.</div>
        ) : (
          <div className="overflow-x-auto rounded-2xl border-2 border-slate-100">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b-2 border-slate-100 text-slate-500 font-bold">
                  <th className="p-4 rounded-tl-2xl whitespace-nowrap">학생 명 / 학번</th>
                  <th className="p-4 whitespace-nowrap">분류 (학년)</th>
                  <th className="p-4 whitespace-nowrap">점수</th>
                  <th className="p-4 rounded-tr-2xl whitespace-nowrap">연습 일시</th>
                </tr>
              </thead>
              <tbody className="divide-y-2 divide-slate-50">
                {records.map((record) => (
                  <tr key={record.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="p-4 font-bold text-slate-700">{record.student_id}</td>
                    <td className="p-4 text-slate-600 font-medium">{record.sentence}</td>
                    <td className="p-4">
                      <span className={`px-4 py-1 rounded-full font-bold text-sm ${
                        record.score >= 90 ? 'bg-green-100 text-green-700' :
                        record.score >= 70 ? 'bg-sky-100 text-sky-700' :
                        'bg-orange-100 text-orange-700'
                      }`}>
                        {record.score}점
                      </span>
                    </td>
                    <td className="p-4 text-slate-500 text-sm">
                      {new Date(record.created_at).toLocaleString('ko-KR')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  );
}

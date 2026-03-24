import type { Metadata } from "next";
import { Jua, Nunito } from "next/font/google";
import "./globals.css";

const jua = Jua({
  variable: "--font-jua",
  subsets: ["latin"],
  weight: "400",
});

const nunito = Nunito({
  variable: "--font-nunito",
  subsets: ["latin"],
  weight: ["400", "700", "900"],
});

export const metadata: Metadata = {
  title: "A.I. P.R.O.C.E.S.S. Tutor",
  description: "Beat the Teacher - 5th Grade English Tutor",
  icons: {
    icon: "🌟",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ko"
      className={`${jua.variable} ${nunito.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col font-jua bg-gradient-to-br from-pink-50 to-sky-100 text-slate-800 selection:bg-rose-200">
        {children}
      </body>
    </html>
  );
}

import type { Metadata } from "next";
import { Plus_Jakarta_Sans, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";

const sans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "EnercoOS 2026 — Enterprise Workstation Distribution | PT Mega Tama Enerco",
    template: "%s | EnercoOS (org.megatama-enerco.com)",
  },
  description:
    "Official portal, documentation hub, and ISO release downloads for EnercoOS 2026 Enterprise Workstation by PT Mega Tama Enerco (org.megatama-enerco.com).",
  metadataBase: new URL("https://org.megatama-enerco.com"),
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${sans.variable} ${mono.variable}`}>
      <body className="flex min-h-screen flex-col font-sans selection:bg-[#0071e3]/40 selection:text-white">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}

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
  keywords: [
    "EnercoOS",
    "Arch Linux",
    "Enterprise Linux",
    "Hyprland",
    "Quickshell",
    "Liquid Glass",
    "MTERP",
    "PT Mega Tama Enerco",
  ],
  authors: [{ name: "PT Mega Tama Enerco", url: "https://org.megatama-enerco.com" }],
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://org.megatama-enerco.com",
    siteName: "EnercoOS Enterprise Workstation",
    title: "EnercoOS 2026 — Liquid Glass Enterprise Linux Workstation",
    description:
      "Open-source enterprise Arch Linux workstation powered by Hyprland, Quickshell Liquid Glass, Calamares 3.3.11, and native MTERP integration.",
    images: [
      {
        url: "/enerco-mac.png",
        width: 1920,
        height: 1080,
        alt: "EnercoOS 2026 Liquid Glass Desktop",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "EnercoOS 2026 — Liquid Glass Enterprise Linux Workstation",
    description:
      "Open-source enterprise Arch Linux workstation powered by Hyprland, Quickshell Liquid Glass, Calamares 3.3.11, and native MTERP integration.",
    images: ["/enerco-mac.png"],
  },
  icons: {
    icon: "/icon.svg",
    apple: "/icon.svg",
  },
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

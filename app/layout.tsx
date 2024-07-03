import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "./components/Header";
import Footer from "./components/Footer";
import { Router } from "next/router";
import App from "next/app";

const inter = Inter({ subsets: ["latin"] });


export const metadata: Metadata = {
  title: "Deepa",
  description: "Your Finance buddy",
  icons: {icon: "/DeepaTransparent-01.png"}
};

const jsonLd =
{
      "@context": "https://schema.org",
      "@type": "Organization",
      "image": "https://www.trydeepa.com//DeepaTransparent-01.png",
    "url": "https://www.newdigit.com",
    "logo": "https://www.trydeepa.com//DeepaTransparent-01.png",
    "name": "Deepa",
      "description": "Empowering a Sustainable Future: Clean & Smart Energy for All",
    "email": "contact@trydeepa.com",
    "telephone": "+2349049500328",
      "address": {
      "@type": "PostalAddress",
      "streetAddress": "7 Lilac Close, Diamond Estate, Cardinal Anthony Olubunmi Okogie Road",
      "addressLocality": "Lagos",
      "addressCountry": "NG",
      "addressRegion": "Eti-Osa, Sangotedo",
      "postalCode": "106104"
    }
}



export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
        <link rel="icon" type="image/png" href="/DeepaTransparent-01.png" sizes="60x30"/>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}

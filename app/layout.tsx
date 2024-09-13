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
      "image": "https:///www.deepa.ng//DeepaTransparent-01.png",
    "url": "https:///www.deepa.ng",
    "logo": "https://www.deepa.ng//DeepaTransparent-01.png",
    "name": "Deepa",
      "description": "Empowering African SMEs",
    "email": "help@trydeepa.ng",
    "telephone": "+2349049500328",
      "address": {
      "@type": "PostalAddress",
      "streetAddress": "Poly Road, Ede, Osun state",
      "addressLocality": "Osun",
      "addressCountry": "NG",
      "addressRegion": "Ede South, Ede",
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

import Image from "next/image";
import Hero from "./components/Hero/index";
import Features from "./components/Features/index";
import FeaturesTab from "./components/FeaturesTab";
import FunFact from "./components/FunFact";
import Integration from "./components/Integration";
import ScrollToTop from "./components/ScrollToTop";
import Footer from "./components/Footer";
import CTA from "./components/CTA";

export default function Home() {
  return (
    <main>
      <Hero></Hero>
      <Features></Features>
      <FeaturesTab></FeaturesTab>
      <FunFact></FunFact>
      <Integration></Integration>
      <CTA></CTA>
    </main>
  );
}

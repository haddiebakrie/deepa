import { FeatureTab } from "@/types/featureTab";
import dark1 from "../../public/images/features/features-dark-01.svg"
import light1 from "../../public/images/features/features-dark-01.svg"

const featuresTabData: FeatureTab[] = [
  {
    id: "tabOne",
    title: "Create Your Online Store with Ease.",
    desc1: `Empower your SME with Deepa’s easy-to-use platform. No coding skills needed—simply drag and drop, add your products, and launch your store in minutes.`,
    desc2: `Key Benefits: Pre-designed templates for a professional look with Mobile-friendly design for global reach and Integration with major e-commerce platforms like Jumia and Amazon (for dropshipping).`,
    image: light1,
    imageDark: dark1,
  },
  {
    id: "tabTwo",
    title: "AI-Powered Insights for Your Business",
    desc1: `Leverage Deepa’s AI assistant to get personalized reports on your store's performance. Analyze sales, inventory, and customer behavior, all with automated suggestions to grow your business.`,
    desc2: `Key Benefits: Sales reports tailored to your specific business goals, including Automated suggestions for improving inventory and marketing and AI chatbot for quick answers and troubleshooting.`,
    image: light1,
    imageDark: dark1,
  },
  {
    id: "tabThree",
    title: "Trustworthy Escrow Payments",
    desc1: `Secure transactions through blockchain-powered escrow payments. Both sellers and buyers are protected, ensuring trust and transparency.`,
    desc2: `Key Benefits: Blockchain technology ensures transparency and reduces fraud. Funds are only released when both parties are satisfied.`,
    image: light1,
    imageDark: dark1,
  },
];

export default featuresTabData;

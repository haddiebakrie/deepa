import Signin from "../../components/Auth/Signin";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Login to go Deepa",
  description: "Login to your account",
  // other metadata
};

const SigninPage = () => {
  return (
    <>
      <Signin />
    </>
  );
};

export default SigninPage;

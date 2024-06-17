import Image from "next/image";
import iconMoon from "../../public/images/icon/icon-moon.svg";
import iconSun from "../../public/images/icon/icon-sun.svg";

const ThemeToggler = () => {

  return (
    <button
      aria-label="theme toggler"
      onClick={() => {}}
      className="bg-gray-2 dark:bg-dark-bg absolute right-17 mr-1.5 flex cursor-pointer items-center justify-center rounded-full text-black dark:text-white lg:static"
    >
      <Image
        src={iconMoon}
        alt="logo"
        width={21}
        height={21}
        className="dark:hidden"
      />

      <Image
        src={iconSun}
        alt="logo"
        width={22}
        height={22}
        className="hidden dark:block"
      />
    </button>
  );
};

export default ThemeToggler;

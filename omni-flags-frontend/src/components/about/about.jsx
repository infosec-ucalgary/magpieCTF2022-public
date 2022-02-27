import React from "react";

import Mission from "./mission";
import Counter from "./counter";
import Executive from "./executive";

const About = () => {
  return (
    <div className="w-full h-screen overflow-y-auto">
      <Mission />
      <Counter />
      <Executive />
    </div>
  );
};

export default About;

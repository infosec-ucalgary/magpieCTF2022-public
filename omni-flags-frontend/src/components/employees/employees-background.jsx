import React from "react";
import { StaticImage } from "gatsby-plugin-image";

import Employees from "./omni_employees"

const EmployeesBackground = () => {
  return (
    <div className="grid">
      <StaticImage
        style={{
          gridArea: "1/1",
        }}
        className="h-screen overflow-hidden"
        layout="fullWidth"
        src="../../images/home-bg.jpg"
        placeholder="blurred"
      />
      <div
        style={{
          gridArea: "1/1",
          position: "relative",
          display: "grid",
        }}
      >
        <Employees />
      </div>
    </div>
  );
};

export default EmployeesBackground;
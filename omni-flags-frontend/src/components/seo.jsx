import React from "react";
import PropTypes from "prop-types";
import { Helmet } from "react-helmet";
import { useStaticQuery, graphql } from "gatsby";

const Seo = ({ description, lang, title }) => {
  const { site } = useStaticQuery(
    graphql`
      query {
        site {
          siteMetadata {
            title
            description
          }
        }
      }
    `
  );

  const metaDescription = description || site.siteMetadata.description;

  return (
    <Helmet
      htmlAttributes={{
        lang,
      }}
      title={title}
      meta={[
        {
          name: `description`,
          content: metaDescription,
        },
        {
          name: `theme-color`,
          content: `#1f1f1f`,
        },
      ]}
    />
  );
};

Seo.defaultProps = {
  lang: `en`,
  description: ``,
};

Seo.propTypes = {
  description: PropTypes.string,
  lang: PropTypes.string,
  title: PropTypes.string.isRequired,
};

export default Seo;

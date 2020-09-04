import React from "react"
import { graphql } from "gatsby"
import './main.css'
export default function Template({
  data, // this prop will be injected by the GraphQL query below.
}) {
  console.log(data)
  const { markdownRemark } = data // data.markdownRemark holds your post data
  const { html } = markdownRemark
  return (
    <div className="markdown-container">
      <div className="markdown-item">
        <div
          className="markdown-item-content"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      </div>
    </div>
  )
}
export const pageQuery = graphql`
  query($slug: String!) {
    markdownRemark(frontmatter: { slug: { eq: $slug } }) {
      html
      frontmatter {
        slug
      }
    }
  }
`
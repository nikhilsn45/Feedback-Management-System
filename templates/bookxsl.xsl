<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
  <html>
  <body>
  <h2>My Book Collection</h2>   
  <table border="1">
      <tr>
        <th>Title</th>
        <th>author</th>
        <th>prize</th>
        <th>year</th>
      </tr>
    <xsl:for-each select="catalogs/book">
      <tr>
        <td><xsl:value-of select="title"/></td>
        <td><xsl:value-of select="author"/></td>
        <td><xsl:value-of select="prize"/></td>
        <td><xsl:value-of select="year"/></td>
      </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>

</xsl:template>

</xsl:stylesheet>
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="#all"
    version="3.0">
    <xsl:output indent="yes"/>
    <xsl:template match="/">
        <xsl:for-each-group group-starting-with="tei:pb[starts-with(@xml:id, 'img')]" select="//tei:ab|//tei:pb">
            <xsl:variable name="facs_id">
                <xsl:value-of select="substring-after(./@facs, '#')"/>
            </xsl:variable>
            <xsl:variable name="image_name">
                <xsl:value-of select="substring-before(data(id($facs_id)/tei:graphic/@url), '.jpg')"/>
            </xsl:variable>
            <xsl:variable name="filename">
                <xsl:value-of select="concat('./tmp/', $image_name, '.xml')"/>
            </xsl:variable>
            
            <xsl:result-document href="{$filename}">
            <TEI>
                <teiHeader>
                    <fileDesc>
                        <titleStmt>
                            <title type="main">
                                <xsl:value-of select="$image_name"/>
                            </title>
                            <principal>stephan.kurz@univie.ac.at</principal>
                        </titleStmt>
                        <publicationStmt>
                            <publisher>tranScriptorium</publisher>
                        </publicationStmt>
                        <seriesStmt>
                            <title>EleonoreMagdalena</title>
                        </seriesStmt>
                        <sourceDesc>
                            <p>TRP document creator: stephan.kurz@univie.ac.at</p>
                        </sourceDesc>
                    </fileDesc>
                </teiHeader>
                <facsimile>
                    <xsl:copy-of select="id($facs_id)"/>
                </facsimile>
                <text>
                    <body>
                        <div type="page" xml:id="{concat('page__', $image_name)}">
                            <xsl:copy-of select="current-group()"/>
                        </div>
                    </body>
                </text>
            </TEI>
            </xsl:result-document>
        </xsl:for-each-group>
    </xsl:template>
    
</xsl:stylesheet>
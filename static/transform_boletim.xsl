<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:param name="date"><xsl:value-of select="request/parametro/boletim/universidade/documento/@emissao"/></xsl:param>
<xsl:template match="/">
                        <boletim xmlns="https://www.w3schools.com">
                            <informacao_pessoal>
                                <nome><xsl:value-of select="request/parametro/boletim/universidade/documento/dados_pessoais/nome"/></nome>
                                <CPF><xsl:value-of select="request/parametro/boletim/universidade/documento/dados_pessoais/cpf"/></CPF>
                                <matricula><xsl:value-of select="request/parametro/boletim/universidade/documento/dados_pessoais/registro_universitario"/></matricula>
                                <endereco><xsl:value-of select="request/parametro/boletim/universidade/documento/dados_pessoais/endereco/tipo_logradouro"/> <xsl:value-of select="request/parametro/boletim/universidade/documento/dados_pessoais/endereco/logradouro"/> <xsl:value-of select="request/parametro/boletim/universidade/documento/dados_pessoais/endereco/numero"/></endereco>
                                <telefone><xsl:value-of select="request/parametro/boletim/universidade/documento/dados_pessoais/contatos/contato[@tipo='telefone celular']/@valor"/></telefone>
                            </informacao_pessoal>
                            <xsl:for-each select="request/parametro/boletim/universidade/documento/periodos">
                                <xsl:for-each select="periodo">
                                <xsl:if test="not(@situacao = 'trancado')">
                                <informacao_periodo>
                                    <data><xsl:value-of select="$date"/></data>
                                    <cr_periodo><xsl:value-of select="@cr"/></cr_periodo>
                                        <xsl:for-each select="aprovado">
                                            <materia>
                                                <nome><xsl:value-of select="@nome"/></nome>
                                                <nota_final><xsl:value-of select="@nota"/></nota_final>
                                                <carga_horaria><xsl:value-of select="@carga_horaria"/></carga_horaria>
                                                <creditos><xsl:value-of select="@creditos"/></creditos>
                                                <situacao_final>Aprovado</situacao_final>
                                            </materia>
                                        </xsl:for-each>
                                        <xsl:for-each select="reprovado">
                                            <materia>
                                                <nome><xsl:value-of select="@nome"/></nome>
                                                <nota_final><xsl:value-of select="@nota"/></nota_final>
                                                <carga_horaria><xsl:value-of select="@carga_horaria"/></carga_horaria>
                                                <creditos><xsl:value-of select="@creditos"/></creditos>
                                                <situacao_final>Reprovado</situacao_final>
                                            </materia>
                                         
                                        </xsl:for-each>
                                </informacao_periodo>
                                </xsl:if>
                                </xsl:for-each>
                            </xsl:for-each>
                        </boletim>
</xsl:template>
</xsl:stylesheet>

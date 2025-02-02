//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.8-b130911.1802 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2019.03.14 at 04:34:17 PM GMT 
//


package uk.ac.ebi.eva.clinvar.model.jaxb;

import java.math.BigInteger;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.datatype.XMLGregorianCalendar;


/**
 * 
 * 				A structure to support reporting of an accession, its version, the date its status changed, and text describing that change.
 * 			
 * 
 * <p>Java class for typeRecordHistory complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="typeRecordHistory">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="Comment" type="{}CommentType" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="Accession" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="Version" use="required" type="{http://www.w3.org/2001/XMLSchema}nonNegativeInteger" />
 *       &lt;attribute name="DateChanged" use="required" type="{http://www.w3.org/2001/XMLSchema}date" />
 *       &lt;attribute name="VariationID" type="{http://www.w3.org/2001/XMLSchema}nonNegativeInteger" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "typeRecordHistory", propOrder = {
    "comment"
})
public class TypeRecordHistory {

    @XmlElement(name = "Comment")
    protected CommentType comment;
    @XmlAttribute(name = "Accession", required = true)
    protected String accession;
    @XmlAttribute(name = "Version", required = true)
    @XmlSchemaType(name = "nonNegativeInteger")
    protected BigInteger version;
    @XmlAttribute(name = "DateChanged", required = true)
    @XmlSchemaType(name = "date")
    protected XMLGregorianCalendar dateChanged;
    @XmlAttribute(name = "VariationID")
    @XmlSchemaType(name = "nonNegativeInteger")
    protected BigInteger variationID;

    /**
     * Gets the value of the comment property.
     * 
     * @return
     *     possible object is
     *     {@link CommentType }
     *     
     */
    public CommentType getComment() {
        return comment;
    }

    /**
     * Sets the value of the comment property.
     * 
     * @param value
     *     allowed object is
     *     {@link CommentType }
     *     
     */
    public void setComment(CommentType value) {
        this.comment = value;
    }

    /**
     * Gets the value of the accession property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAccession() {
        return accession;
    }

    /**
     * Sets the value of the accession property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAccession(String value) {
        this.accession = value;
    }

    /**
     * Gets the value of the version property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getVersion() {
        return version;
    }

    /**
     * Sets the value of the version property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setVersion(BigInteger value) {
        this.version = value;
    }

    /**
     * Gets the value of the dateChanged property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getDateChanged() {
        return dateChanged;
    }

    /**
     * Sets the value of the dateChanged property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setDateChanged(XMLGregorianCalendar value) {
        this.dateChanged = value;
    }

    /**
     * Gets the value of the variationID property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getVariationID() {
        return variationID;
    }

    /**
     * Sets the value of the variationID property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setVariationID(BigInteger value) {
        this.variationID = value;
    }

}

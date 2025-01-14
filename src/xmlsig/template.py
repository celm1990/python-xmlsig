# -*- encoding: utf-8 -*-
# © 2017 Creu Blanca
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from lxml import etree

from .constants import ID_ATTR, NS_MAP, DSigNs
from .utils import create_node


def add_key_name(node, name=False):
    node.text = "\n"
    key_name = create_node("KeyName", node, DSigNs, tail="\n")
    if name:
        key_name.text = name
    return key_name


def add_key_value(node):
    return create_node("KeyValue", node, DSigNs, tail="\n")


def add_reference(node, digest_method, name=False, uri=False, uri_type=False):
    reference = create_node(
        "Reference",
        node.find("{" + DSigNs + "}SignedInfo"),
        DSigNs,
        tail="\n",
        text="\n",
    )
    if name:
        reference.set(ID_ATTR, name)
    if uri == "":
        reference.set("URI", "")
    if uri:
        reference.set("URI", uri)
    if uri_type:
        reference.set("Type", uri_type)
    digest_method_node = create_node("DigestMethod", reference, DSigNs, tail="\n")
    digest_method_node.set("Algorithm", digest_method)
    create_node("DigestValue", reference, DSigNs, tail="\n")
    return reference


def add_transform(node, transform):
    transforms_node = node.find("ds:Transforms", namespaces=NS_MAP)
    if transforms_node is None:
        transforms_node = create_node("Transforms", ns=DSigNs, tail="\n", text="\n")
        node.insert(0, transforms_node)
    transform_node = create_node("Transform", transforms_node, DSigNs, tail="\n")
    transform_node.set("Algorithm", transform)
    return transform_node


def add_x509_data(node):
    node.text = "\n"
    return create_node("X509Data", node, DSigNs, tail="\n")


def create(c14n_method=False, sign_method=False, name=False, ns="ds"):
    node = etree.Element(etree.QName(DSigNs, "Signature"), nsmap={ns: DSigNs})
    node.text = "\n"
    if name:
        node.set(ID_ATTR, name)
    signed_info = create_node("SignedInfo", node, DSigNs, tail="\n", text="\n")
    canonicalization = create_node(
        "CanonicalizationMethod", signed_info, DSigNs, tail="\n"
    )
    canonicalization.set("Algorithm", c14n_method)
    signature_method = create_node("SignatureMethod", signed_info, DSigNs, tail="\n")
    signature_method.set("Algorithm", sign_method)
    create_node("SignatureValue", node, DSigNs, tail="\n")
    return node


def ensure_key_info(node, name=False):
    key_info = node.find("{" + DSigNs + "}KeyInfo")
    if key_info is None:
        key_info = create_node("KeyInfo", ns=DSigNs, tail="\n")
        node.insert(2, key_info)
    if name:
        key_info.set(ID_ATTR, name)
    return key_info


def x509_data_add_certificate(node):
    node.text = "\n"
    return create_node("X509Certificate", node, DSigNs, tail="\n")


def x509_data_add_crl(node):
    node.text = "\n"
    return create_node("X509CRL", node, DSigNs, tail="\n")


def x509_data_add_issuer_serial(node):
    node.text = "\n"
    return create_node("X509IssuerSerial", node, DSigNs, tail="\n")


def x509_data_add_ski(node):
    node.text = "\n"
    return create_node("X509SKI", node, DSigNs, tail="\n")


def x509_data_add_subject_name(node):
    node.text = "\n"
    return create_node("X509SubjectName", node, DSigNs, tail="\n")


def x509_issuer_serial_add_issuer_name(node):
    node.text = "\n"
    return create_node("X509IssuerName", node, DSigNs, tail="\n")


def x509_issuer_serial_add_serial_number(node):
    node.text = "\n"
    return create_node("X509SerialNumber", node, DSigNs, tail="\n")

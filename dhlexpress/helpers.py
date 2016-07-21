# -*- coding: utf-8 -*-

from lxml import etree


BASE = '/ShipmentResponse%s'
HEADER = BASE % '/Response/ServiceHeader%s'
PIECES = BASE % '/Pieces%s'
BARCODES = BASE % '/Barcodes%s'
CONSIGNEE = BASE % '/Consignee%s'
CONSIGNEE_CONTACT = CONSIGNEE % '/Contact%s'
SHIPPER = BASE % '/Shipper%s'
SHIPPER_CONTACT = SHIPPER % '/Contact%s'


class XMLNamespaces:
   req = 'http://www.dhl.com'
   xsi = 'http://www.w3.org/2001/XMLSchema-instance'
   schemaLocation = 'http://www.dhl.com ship-val-global-req.xsd'
   schemaVersion = '1.0'


def xpath_ns(tree, expr):
    "Parse a simple expression and prepend namespace wildcards where unspecified."
    qual = lambda n: n if not n or ':' in n else '*[local-name() = "%s"]' % n
    expr = '/'.join(qual(n) for n in expr.split('/'))
    nsmap = dict((k, v) for k, v in tree.nsmap.items() if k)
    return tree.xpath(expr, namespaces=nsmap)


def quote_req(arg1, arg2):
    root = etree.Element(
            etree.QName(XMLNamespaces.req, 'DCTRequest'),
            nsmap = {"req": XMLNamespaces.req}
        )
    capability = etree.SubElement(root, "GetCapability")
    request = etree.SubElement(capability, "Request")

    serviceheader = etree.SubElement(request, "ServiceHeader")

    msgtime = etree.SubElement(serviceheader, "MessageTime")
    msgtime.text = "2011-03-16T14:57:20-07:00"
    msgref = etree.SubElement(serviceheader, "MessageReference")
    msgref.text = "718688fff23f46f49d7cf9b67cd40d4e"
    siteid = etree.SubElement(serviceheader, "SiteID")
    siteid.text = arg1
    password = etree.SubElement(serviceheader, "Password")
    password.text = arg2

    _from = etree.SubElement(capability, "From")

    countrycode = etree.SubElement(_from, "CountryCode")
    countrycode.text = "US"
    postalcode = etree.SubElement(_from, "Postalcode")
    postalcode.text = "85281"
    city = etree.SubElement(_from, "City")
    city.text = "Tempe"

    bkgdetails = etree.SubElement(capability, "BkgDetails")
    payment_country = etree.SubElement(bkgdetails, "PaymentCountryCode")
    payment_country.text = "US"
    date = etree.SubElement(bkgdetails, "Date")
    date.text = "2016-07-20"
    ready_time = etree.SubElement(bkgdetails, "ReadyTime")
    ready_time.text = "PT9H"
    dimension_unit = etree.SubElement(bkgdetails, "DimensionUnit")
    dimension_unit.text = "IN"
    weight_unit = etree.SubElement(bkgdetails, "WeightUnit")
    weight_unit.text = "LB"

    pieces = etree.SubElement(bkgdetails, "Pieces")
    piece = etree.SubElement(pieces, "Piece")

    pieceid = etree.SubElement(piece, "PieceID")
    pieceid.text = "1"
    height = etree.SubElement(piece, "Height")
    height.text = "1"
    depth = etree.SubElement(piece, "Depth")
    depth.text = "1"
    width = etree.SubElement(piece, "Width")
    width.text = "1"
    weight = etree.SubElement(piece, "Weight")
    weight.text = "1"

    is_dutiable = etree.SubElement(bkgdetails, "IsDutiable")
    is_dutiable.text = "Y"
    qtdshp = etree.SubElement(bkgdetails, "QtdShp")

    qtdshpexchrg = etree.SubElement(qtdshp, "QtdShpExChrg")
    special_service_type = etree.SubElement(qtdshpexchrg, "SpecialServiceType")
    special_service_type.text = "OSINFO"

    to = etree.SubElement(capability, "To")
    country_code = etree.SubElement(to, "CountryCode")
    country_code.text = "FR"
    postal_code = etree.SubElement(to, "Postalcode")
    postal_code.text = "75001"
    city = etree.SubElement(to, "City")
    city.text = "Paris"

    dutiable = etree.SubElement(capability, "Dutiable")
    declared_currency = etree.SubElement(dutiable, "DeclaredCurrency")
    declared_currency.text = "USD"
    declared_value = etree.SubElement(dutiable, "DeclaredValue")
    declared_value.text = "10"
    return etree.tostring(root, xml_declaration=True, encoding='utf-8')

def shipment_req(arg1, arg2, arg3):
    root = etree.Element(
        etree.QName(XMLNamespaces.req, 'ShipmentRequest'),
        attrib={
            "{" + XMLNamespaces.xsi + "}schemaLocation" : XMLNamespaces.schemaLocation,
            "schemaVersion" : XMLNamespaces.schemaVersion
        },
        nsmap = {
            "req": XMLNamespaces.req,
            "xsi": XMLNamespaces.xsi,
        }
    )
    request = etree.SubElement(root, "Request")
    serviceheader = etree.SubElement(request, "ServiceHeader")

    msgtime = etree.SubElement(serviceheader, "MessageTime")
    msgtime.text = "2011-03-16T14:57:20-07:00"
    msgref = etree.SubElement(serviceheader, "MessageReference")
    msgref.text = "718688fff23f46f49d7cf9b67cd40d4e"
    siteid = etree.SubElement(serviceheader, "SiteID")
    siteid.text = arg1
    password = etree.SubElement(serviceheader, "Password")
    password.text = arg2

    region_code = etree.SubElement(root, "RegionCode")
    region_code.text = "EU"
    req_pickup_time = etree.SubElement(root, "RequestedPickupTime")
    req_pickup_time.text = "Y"
    new_shipper = etree.SubElement(root, "NewShipper")
    new_shipper.text = "Y"
    lang_code = etree.SubElement(root, "LanguageCode")
    lang_code.text = "en"

    pieces_enabled = etree.SubElement(root, "PiecesEnabled")
    pieces_enabled.text = "Y"

    billing = etree.SubElement(root, "Billing")
    shipper_acc_no = etree.SubElement(billing, "ShipperAccountNumber")
    shipper_acc_no.text = arg3
    shipper_payment_type = etree.SubElement(billing, "ShippingPaymentType")
    shipper_payment_type.text = "S"
    billing_acc_no = etree.SubElement(billing, "BillingAccountNumber")
    billing_acc_no.text = arg3
    duty_payment_type = etree.SubElement(billing, "DutyPaymentType")
    duty_payment_type.text = "R"

    consignee = etree.SubElement(root, "Consignee")
    company_name = etree.SubElement(consignee, "CompanyName")
    company_name.text = "Consignee Company Name"
    address_line = etree.SubElement(consignee, "AddressLine")
    address_line.text = "Consignee Address line 1"
    city = etree.SubElement(consignee, "City")
    city.text = "Tokyo"
    postal_code = etree.SubElement(consignee, "PostalCode")
    postal_code.text = "1000001"
    country_code = etree.SubElement(consignee, "CountryCode")
    country_code.text = "JP"
    country_name = etree.SubElement(consignee, "CountryName")
    country_name.text = "Japan"
    contact = etree.SubElement(consignee, "Contact")
    person_name = etree.SubElement(contact, "PersonName")
    person_name.text = "Consignee Contact"
    phone_number = etree.SubElement(contact, "PhoneNumber")
    phone_number.text = "1234567890"

    dutiable = etree.SubElement(root, "Dutiable")
    declared_value = etree.SubElement(dutiable, "DeclaredValue")
    declared_value.text = "1000"
    declared_currency = etree.SubElement(dutiable, "DeclaredCurrency")
    declared_currency.text = "USD"
    terms_of_trade = etree.SubElement(dutiable, "TermsOfTrade")
    terms_of_trade.text = "DAP"
    filing = etree.SubElement(dutiable, "Filing")
    filing_type = etree.SubElement(filing, "FilingType")
    filing_type.text = "FTR"
    ftsr = etree.SubElement(filing, "FTSR")
    ftsr.text = "30.37(a)"

    reference = etree.SubElement(root, "Reference")
    reference_id = etree.SubElement(reference, "ReferenceID")
    reference_id.text = "Shipment Reference Type"

    shipment_details = etree.SubElement(root, "ShipmentDetails")
    no_pieces = etree.SubElement(shipment_details, "NumberOfPieces")
    no_pieces.text = "1"
    pieces = etree.SubElement(shipment_details, "Pieces")
    
    piece = etree.SubElement(pieces, "Piece")
    pieceid = etree.SubElement(piece, "PieceID")
    pieceid.text = "1"
    weight = etree.SubElement(piece, "Weight")
    weight.text = "20"
    width = etree.SubElement(piece, "Width")
    width.text = "10"
    height = etree.SubElement(piece, "Height")
    height.text = "10"
    depth = etree.SubElement(piece, "Depth")
    depth.text = "10"

    weight = etree.SubElement(shipment_details, "Weight")
    weight.text = "20"
    weight_unit = etree.SubElement(shipment_details, "WeightUnit")
    weight_unit.text = "L"
    global_product_code = etree.SubElement(shipment_details, "GlobalProductCode")
    global_product_code.text = "P"
    local_product_code = etree.SubElement(shipment_details, "LocalProductCode")
    local_product_code.text = "P"
    date = etree.SubElement(shipment_details, "Date")
    date.text = "2016-07-21"
    contents = etree.SubElement(shipment_details, "Contents")
    contents.text = "Shipment Description Here"
    door_to = etree.SubElement(shipment_details, "DoorTo")
    door_to.text = "DA"
    dimension_unit = etree.SubElement(shipment_details, "DimensionUnit")
    dimension_unit.text = "I"
    insured_amount = etree.SubElement(shipment_details, "InsuredAmount")
    insured_amount.text = "4"
    package_type = etree.SubElement(shipment_details, "PackageType")
    package_type.text = "EE"
    is_dutiable = etree.SubElement(shipment_details, "IsDutiable")
    is_dutiable.text = "Y"
    currency_code = etree.SubElement(shipment_details, "CurrencyCode")
    currency_code.text = "USD"

    shipper = etree.SubElement(root, "Shipper")
    shipper_id = etree.SubElement(shipper, "ShipperID")
    shipper_id.text = arg3
    company_name = etree.SubElement(shipper, "CompanyName")
    company_name.text = "Shipper Company Name"
    reg_acc = etree.SubElement(shipper, "RegisteredAccount")
    reg_acc.text = arg3
    address_line = etree.SubElement(shipper, "AddressLine")
    address_line.text = "Shipper AddressLine 1"
    city = etree.SubElement(shipper, "City")
    city.text = "Tempe"

    division = etree.SubElement(shipper, "Division")
    division_code = etree.SubElement(shipper, "DivisionCode")
    postal_code = etree.SubElement(shipper, "PostalCode")
    postal_code.text = "1000001"
    origin_service_code = etree.SubElement(shipper, "OriginServiceAreaCode")
    origin_service_code.text = "100"
    origin_facility_code = etree.SubElement(shipper, "OriginFacilityCode")
    origin_facility_code.text = "100"
    country_code = etree.SubElement(shipper, "CountryCode")
    country_code.text = "US"
    country_name = etree.SubElement(shipper, "CountryName")
    country_name.text = "United States"
    federal_tax_id = etree.SubElement(shipper, "FederalTaxId")
    federal_tax_id.text = "AF354HBU"
    state_tax_id = etree.SubElement(shipper, "StateTaxId")
    state_tax_id.text = "79JNG7d"
    contact = etree.SubElement(shipper, "Contact")
    person_name = etree.SubElement(contact, "PersonName")
    person_name.text = "Shipper Contact"
    phone_number = etree.SubElement(contact, "PhoneNumber")
    phone_number.text = "1234567890"
    suburb = etree.SubElement(shipper, "Suburb")
    suburb.text = "Suburb"

    label_image_format = etree.SubElement(root, "LabelImageFormat")
    label_image_format.text = "PDF"

    return etree.tostring(root, xml_declaration=True, encoding='utf-8')

def shipment_resp(content):
    xml = etree.fromstring(content)
    # print etree.tostring(xml, pretty_print=True)

    MessageTime = xpath_ns(xml, HEADER % '/MessageTime')[0].text
    MessageReference = xpath_ns(xml, HEADER % '/MessageReference')[0].text
    SiteID = xpath_ns(xml, HEADER % '/SiteID')[0].text

    ActionNote = xpath_ns(xml, BASE % '/Note/ActionNote')[0].text
    AirwayBillNumber = xpath_ns(xml, BASE % '/AirwayBillNumber')[0].text
    BillingCode = xpath_ns(xml, BASE % '/BillingCode')[0].text
    CurrencyCode = xpath_ns(xml, BASE % '/CurrencyCode')[0].text
    Rated = xpath_ns(xml, BASE % '/Rated')[0].text
    WeightUnit = xpath_ns(xml, BASE % '/WeightUnit')[0].text
    CountryCode = xpath_ns(xml, BASE % '/CountryCode')[0].text

    DataIdentifier = xpath_ns(xml, PIECES % '/Piece/DataIdentifier')[0].text
    LicensePlate = xpath_ns(xml, PIECES % '/Piece/LicensePlate')[0].text
    LicensePlateBarCode = xpath_ns(xml, PIECES % '/Piece/LicensePlateBarCode')[0].text

    AWBBarCode = xpath_ns(xml, BARCODES % '/AWBBarCode')[0].text
    OriginDestnBarcode = xpath_ns(xml, BARCODES % '/OriginDestnBarcode')[0].text
    DHLRoutingBarCode = xpath_ns(xml, BARCODES % '/DHLRoutingBarCode')[0].text

    Contents = xpath_ns(xml, BASE % '/Contents')[0].text

    Consignee_CompanyName = xpath_ns(xml, CONSIGNEE % '/CompanyName')[0].text
    Consignee_CountryCode = xpath_ns(xml, CONSIGNEE % '/CountryCode')[0].text
    Consignee_CountryName = xpath_ns(xml, CONSIGNEE % '/CountryName')[0].text

    Consignee_PersonName = xpath_ns(xml, CONSIGNEE_CONTACT % '/PersonName')[0].text
    Consignee_PhoneNumber = xpath_ns(xml, CONSIGNEE_CONTACT % '/PhoneNumber')[0].text

    ShipperID = xpath_ns(xml, SHIPPER % '/ShipperID')[0].text
    Shipper_CompanyName = xpath_ns(xml, SHIPPER % '/CompanyName')[0].text
    Shipper_AddressLine = xpath_ns(xml, SHIPPER % '/AddressLine')[0].text
    Shipper_CountryCode = xpath_ns(xml, SHIPPER % '/CountryCode')[0].text
    Shipper_CountryName = xpath_ns(xml, SHIPPER % '/CountryName')[0].text

    Shipper_PersonName = xpath_ns(xml, SHIPPER_CONTACT % '/PersonName')[0].text
    Shipper_PhoneNumber = xpath_ns(xml, SHIPPER_CONTACT % '/PhoneNumber')[0].text

    CustomerID = xpath_ns(xml, BASE % '/CustomerID')[0].text
    ShipmentDate = xpath_ns(xml, BASE % '/ShipmentDate')[0].text
    GlobalProductCode = xpath_ns(xml, BASE % '/GlobalProductCode')[0].text
    
    parsed_resp = {
        'MessageTime': MessageTime,
        'MessageReference': MessageReference,
        'SiteID': SiteID,
        'ActionNote': ActionNote,
        'AirwayBillNumber': AirwayBillNumber,
        'BillingCode': BillingCode,
        'CurrencyCode': CurrencyCode,
        'Rated': Rated,
        'WeightUnit': WeightUnit,
        'CountryCode': CountryCode,
        'DataIdentifier': DataIdentifier,
        'LicensePlate': LicensePlate,
        'LicensePlateBarCode': LicensePlateBarCode,
        'AWBBarCode': AWBBarCode,
        'OriginDestnBarcode': OriginDestnBarcode,
        'DHLRoutingBarCode': DHLRoutingBarCode,
        'Contents': Contents,
        'Consignee_CompanyName': Consignee_CompanyName,
        'Consignee_CountryCode': Consignee_CountryCode,
        'Consignee_CountryName': Consignee_CountryName,
        'Consignee_PersonName': Consignee_PersonName,
        'Consignee_PhoneNumber': Consignee_PhoneNumber,
        'ShipperID': ShipperID,
        'Shipper_CompanyName': Shipper_CompanyName,
        'Shipper_AddressLine': Shipper_AddressLine,
        'Shipper_CountryCode': Shipper_CountryCode,
        'Shipper_CountryName': Shipper_CountryName,
        'Shipper_PersonName': Shipper_PersonName,
        'Shipper_PhoneNumber': Shipper_PhoneNumber,
        'CustomerID': CustomerID,
        'ShipmentDate': ShipmentDate,
        'GlobalProductCode': GlobalProductCode,
    }
    return parsed_resp
"""
Exact coordinates for all 5 gas detector products
Extracted using pdfminer.six from the original PDF templates
"""

# Coordinate mappings for each product
# All coordinates are in PDF points (1/72 inch) from bottom-left origin

PRODUCT_COORDINATES = {
    "D4PQ": {  # MGC-S+ (MGC-SIMPLEPLUS)
        "page1": {
            "serial": {"x": 395.92, "y": 642.58, "size": 14},
            "activation_date": {"x": 447.71, "y": 633.03, "size": 9},
            "lot": {"x": 95.75, "y": 406.58, "size": 13},
            "gas_prod": {"x": 169.46, "y": 389.64, "size": 10},
            "calibration": {"x": 167.08, "y": 315.42, "size": 13},
        },
        "page2": {
            "serial": {"x": 382.82, "y": 677.62, "size": 14},
            "activation_boxes": {"x": 340, "y": 480, "spacing": 20},
            "expiration_boxes": {"x": 340, "y": 400, "spacing": 20},
        }
    },
    
    "SOSP": {  # SGC-O (Single Gas Clip O2)
        "page1": {
            "serial": {"x": 395.92, "y": 636.58, "size": 14},
            "activation_date": {"x": 447.71, "y": 627.03, "size": 9},
            "lot": {"x": 95.75, "y": 406.58, "size": 13},
            "gas_prod": {"x": 169.46, "y": 389.64, "size": 10},
            "calibration": {"x": 167.08, "y": 315.42, "size": 13},
        },
        "page2": {
            "serial": {"x": 382.82, "y": 687.62, "size": 14},
            "activation_boxes": {"x": 340, "y": 480, "spacing": 20},
            "expiration_boxes": {"x": 340, "y": 400, "spacing": 20},
        }
    },
    
    "SCSQ": {  # SGC-C (Single Gas Clip CO)
        "page1": {
            "serial": {"x": 395.92, "y": 636.58, "size": 14},
            "activation_date": {"x": 447.71, "y": 627.03, "size": 9},
            "lot": {"x": 95.75, "y": 406.58, "size": 13},
            "gas_prod": {"x": 169.46, "y": 389.64, "size": 10},
            "calibration": {"x": 167.08, "y": 315.42, "size": 13},
        },
        "page2": {
            "serial": {"x": 382.82, "y": 687.62, "size": 14},
            "activation_boxes": {"x": 340, "y": 480, "spacing": 20},
            "expiration_boxes": {"x": 340, "y": 400, "spacing": 20},
        }
    },
    
    "D4SQ": {  # MGC-S (MGC-SIMPLE)
        "page1": {
            "serial": {"x": 395.92, "y": 642.58, "size": 14},
            "activation_date": {"x": 447.71, "y": 633.03, "size": 9},
            "lot": {"x": 95.75, "y": 406.58, "size": 13},
            "gas_prod": {"x": 169.46, "y": 389.64, "size": 10},
            "calibration": {"x": 167.08, "y": 315.42, "size": 13},
        },
        "page2": {
            "serial": {"x": 382.82, "y": 677.62, "size": 14},
            "activation_boxes": {"x": 340, "y": 480, "spacing": 20},
            "expiration_boxes": {"x": 340, "y": 400, "spacing": 20},
        }
    },
    
    "SHSP": {  # SGC-H (Single Gas Clip H2S)
        "page1": {
            "serial": {"x": 395.92, "y": 636.58, "size": 14},
            "activation_date": {"x": 447.71, "y": 627.03, "size": 9},
            "lot": {"x": 95.75, "y": 406.58, "size": 13},
            "gas_prod": {"x": 169.46, "y": 389.64, "size": 10},
            "calibration": {"x": 167.08, "y": 315.42, "size": 13},
        },
        "page2": {
            "serial": {"x": 382.82, "y": 687.62, "size": 14},
            "activation_boxes": {"x": 340, "y": 480, "spacing": 20},
            "expiration_boxes": {"x": 340, "y": 400, "spacing": 20},
        }
    },
}


def get_coordinates(prefix):
    """
    Get coordinates for a specific product prefix
    
    Args:
        prefix (str): Product prefix (D4PQ, SOSP, SCSQ, D4SQ, SHSP)
    
    Returns:
        dict: Coordinate mapping for the product
    """
    return PRODUCT_COORDINATES.get(prefix, PRODUCT_COORDINATES["D4PQ"])

"""
Exact coordinates for all 5 gas detector products
Extracted and calibrated from the original PDF templates
v3.3 - Fine-tuned positioning to avoid covering labels
"""

# Coordinate mappings for each product
# All coordinates are in PDF points (1/72 inch) from bottom-left origin
# A4 page size: 595 x 842 points

PRODUCT_COORDINATES = {
    "D4PQ": {  # MGC-S+ (MGC-SIMPLEPLUS)
        "page1": {
            # Serial number in the "Serial Number" box
            "serial": {"x": 405, "y": 642, "size": 14, "cover_x": 403, "cover_w": 110, "cover_h": 18},
            # Activation date - positioned right of "Activate before:" label
            "activation_date": {"x": 450, "y": 626, "size": 9, "cover_x": 448, "cover_w": 60, "cover_h": 14},
            # Lot number - positioned at start of lot value area
            "lot": {"x": 77, "y": 407, "size": 13, "cover_x": 75, "cover_w": 105, "cover_h": 18},
            # Gas production date - after "Gas Production:" label (starts around x=169)
            "gas_prod": {"x": 172, "y": 389, "size": 10, "cover_x": 170, "cover_w": 65, "cover_h": 14},
            # Calibration date - after "Calibrated on :" label (starts around x=167)
            "calibration": {"x": 170, "y": 315, "size": 13, "cover_x": 168, "cover_w": 80, "cover_h": 18},
        },
        "page2": {
            # Serial number after "sn :" label
            "serial": {"x": 382, "y": 677, "size": 14, "cover_x": 378, "cover_w": 110, "cover_h": 18},
            # Activation date boxes (10 chars: DD.MM.YYYY)
            "activation_boxes": {"x": 358, "y": 528, "spacing": 17.3, "size": 11},
            # Expiration date boxes (10 chars: DD.MM.YYYY)
            "expiration_boxes": {"x": 358, "y": 368, "spacing": 17.3, "size": 11},
        }
    },

    "SOSP": {  # SGC-O (Single Gas Clip O2)
        "page1": {
            "serial": {"x": 405, "y": 636, "size": 14, "cover_x": 403, "cover_w": 110, "cover_h": 18},
            "activation_date": {"x": 450, "y": 620, "size": 9, "cover_x": 448, "cover_w": 60, "cover_h": 14},
            "lot": {"x": 77, "y": 407, "size": 13, "cover_x": 75, "cover_w": 105, "cover_h": 18},
            "gas_prod": {"x": 172, "y": 389, "size": 10, "cover_x": 170, "cover_w": 65, "cover_h": 14},
            "calibration": {"x": 170, "y": 315, "size": 13, "cover_x": 168, "cover_w": 80, "cover_h": 18},
        },
        "page2": {
            "serial": {"x": 382, "y": 687, "size": 14, "cover_x": 378, "cover_w": 110, "cover_h": 18},
            "activation_boxes": {"x": 358, "y": 528, "spacing": 17.3, "size": 11},
            "expiration_boxes": {"x": 358, "y": 368, "spacing": 17.3, "size": 11},
        }
    },

    "SCSQ": {  # SGC-C (Single Gas Clip CO)
        "page1": {
            "serial": {"x": 405, "y": 636, "size": 14, "cover_x": 403, "cover_w": 110, "cover_h": 18},
            "activation_date": {"x": 450, "y": 620, "size": 9, "cover_x": 448, "cover_w": 60, "cover_h": 14},
            "lot": {"x": 77, "y": 407, "size": 13, "cover_x": 75, "cover_w": 105, "cover_h": 18},
            "gas_prod": {"x": 172, "y": 389, "size": 10, "cover_x": 170, "cover_w": 65, "cover_h": 14},
            "calibration": {"x": 170, "y": 315, "size": 13, "cover_x": 168, "cover_w": 80, "cover_h": 18},
        },
        "page2": {
            "serial": {"x": 382, "y": 687, "size": 14, "cover_x": 378, "cover_w": 110, "cover_h": 18},
            "activation_boxes": {"x": 358, "y": 528, "spacing": 17.3, "size": 11},
            "expiration_boxes": {"x": 358, "y": 368, "spacing": 17.3, "size": 11},
        }
    },

    "D4SQ": {  # MGC-S (MGC-SIMPLE)
        "page1": {
            "serial": {"x": 405, "y": 642, "size": 14, "cover_x": 403, "cover_w": 110, "cover_h": 18},
            "activation_date": {"x": 450, "y": 626, "size": 9, "cover_x": 448, "cover_w": 60, "cover_h": 14},
            "lot": {"x": 77, "y": 407, "size": 13, "cover_x": 75, "cover_w": 105, "cover_h": 18},
            "gas_prod": {"x": 172, "y": 389, "size": 10, "cover_x": 170, "cover_w": 65, "cover_h": 14},
            "calibration": {"x": 170, "y": 315, "size": 13, "cover_x": 168, "cover_w": 80, "cover_h": 18},
        },
        "page2": {
            "serial": {"x": 382, "y": 677, "size": 14, "cover_x": 378, "cover_w": 110, "cover_h": 18},
            "activation_boxes": {"x": 358, "y": 528, "spacing": 17.3, "size": 11},
            "expiration_boxes": {"x": 358, "y": 368, "spacing": 17.3, "size": 11},
        }
    },

    "SHSP": {  # SGC-H (Single Gas Clip H2S)
        "page1": {
            "serial": {"x": 405, "y": 636, "size": 14, "cover_x": 403, "cover_w": 110, "cover_h": 18},
            "activation_date": {"x": 450, "y": 620, "size": 9, "cover_x": 448, "cover_w": 60, "cover_h": 14},
            "lot": {"x": 77, "y": 407, "size": 13, "cover_x": 75, "cover_w": 105, "cover_h": 18},
            "gas_prod": {"x": 172, "y": 389, "size": 10, "cover_x": 170, "cover_w": 65, "cover_h": 14},
            "calibration": {"x": 170, "y": 315, "size": 13, "cover_x": 168, "cover_w": 80, "cover_h": 18},
        },
        "page2": {
            "serial": {"x": 382, "y": 687, "size": 14, "cover_x": 378, "cover_w": 110, "cover_h": 18},
            "activation_boxes": {"x": 358, "y": 528, "spacing": 17.3, "size": 11},
            "expiration_boxes": {"x": 358, "y": 368, "spacing": 17.3, "size": 11},
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

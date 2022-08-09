resource "azurerm_policy_definition" "allowed-location-definition" {
  name         = "location-policy-definition-${var.tp_name}-${var.instance_id}"
  policy_type  = "Custom"
  mode         = "All"
  display_name  = "eastus-location-policy"
  policy_rule = <<POLICY_RULE
    {
    "if": {
      "not": {
        "field": "location",
        "equals": "eastus"
      }
    },
    "then": {
      "effect": "deny"
    }
  }
POLICY_RULE
}

resource "azurerm_policy_definition" "allowed-sku-definition" {   
  name         = "sku-policy-definition-${var.tp_name}-${var.instance_id}"
  policy_type  = "Custom"
  mode         = "All"
  display_name  = "sku-policy"
  policy_rule = <<POLICY_RULE
	  {
  	"if": {
           "allOf": [
                       {
                        "field": "type",
                         "equals": "Microsoft.Compute/virtualMachines"                   
                       },
                        {
                        "not": {
                                "field": "Microsoft.Compute/virtualMachines/sku.name",
                                "equals": "Standard_D2s_v3"                                
                                }
                         } 
                    ]
        },
            "then": {
                "effect": "Deny"
            }
    }
POLICY_RULE
}
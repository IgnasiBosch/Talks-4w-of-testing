"""

schema example:
{
  "id": "in_1036Vr2eZvKYlo2CfjuUHA94",
  "object": "invoice",
  "amount_due": 0,
  "amount_paid": 0,
  "amount_remaining": 0,
  "application_fee": null,
  "attempt_count": 0,
  "attempted": true,
  "billing": "charge_automatically",
  "billing_reason": null,
  "charge": null,
  "closed": true,
  "currency": "usd",
  "customer": "cus_D6nocXHQTVqNkf",
  "date": 1386790772,
  "description": null,
  "discount": null,
  "due_date": null,
  "ending_balance": null,
  "forgiven": false,
  "hosted_invoice_url": null,
  "invoice_pdf": null,
  "lines": {
    "data": [
      {
        "id": "sli_eb2591c30b4085",
        "object": "line_item",
        "amount": 5465,
        "currency": "usd",
        "description": "1 × vvv (at $54.65 / every 5 weeks)",
        "discountable": true,
        "livemode": false,
        "metadata": {
        },
        "period": {
          "end": 1450726772,
          "start": 1447702772
        },
        "plan": {
          "id": "40",
          "object": "plan",
          "active": true,
          "aggregate_usage": null,
          "amount": 5465,
          "billing_scheme": "per_unit",
          "created": 1386694689,
          "currency": "usd",
          "interval": "week",
          "interval_count": 5,
          "livemode": false,
          "metadata": {
            "charset": "utf-8",
            "content": "40"
          },
          "nickname": null,
          "product": "prod_BTcfj5EqyqxDVn",
          "tiers": null,
          "tiers_mode": null,
          "transform_usage": null,
          "trial_period_days": 5,
          "usage_type": "licensed"
        },
        "proration": false,
        "quantity": 1,
        "subscription": "sub_36VrPHS2vVxJMq",
        "subscription_item": "si_18SfBn2eZvKYlo2C1fwOImYF",
        "type": "subscription"
      }
    ],
    "has_more": false,
    "object": "list",
    "url": "/v1/invoices/in_1036Vr2eZvKYlo2CfjuUHA94/lines"
  },
  "livemode": false,
  "metadata": {
  },
  "next_payment_attempt": null,
  "number": null,
  "paid": true,
  "period_end": 1386790772,
  "period_start": 1386790772,
  "receipt_number": null,
  "starting_balance": 0,
  "statement_descriptor": null,
  "subscription": "sub_36VrPHS2vVxJMq",
  "subtotal": 0,
  "tax": null,
  "tax_percent": null,
  "total": 0,
  "webhooks_delivered_at": 1386790772
}


"""


def validate_period(line_item):
    start = line_item['period']['start']
    end = line_item['period']['end']

    return start < end


def validate_plan(line_item):
    plan = line_item['plan']
    
    return plan.get('active', False)


def validate_line(line_item):
    return validate_period(line_item) and validate_plan(line_item)


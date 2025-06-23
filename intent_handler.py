from logger import logger


def get_intent(tokens, raw_text):
    try:
        intents = {
            'demand': ['demand', 'consumption', 'average', 'load', 'forecast', 'electricity'],

            'mod': ['mod', 'mod price', 'dispatch price', 'grid', 'dispatch', 'moment', 'last_price', 'last price', 'moment', 'moment of dispatch',
                    'dispatch price', 'mod rate', ],

            'iex': ['iex', 'iex price', 'market price', 'exchange', 'market rate', 'exchange', 'iex cost', 'indian energy exchange', 'exchange'],

            'procurement': ['procurement', 'purchase', 'buy', 'bought', 'procure', 'procured', 'power purchase cost',
                           'procurement info', 'procurement price'],

            'cost per block': ['cost per block','cost rate', 'cost_per_block', 'block cost', 'rate per block', 'block rate'],

            'plant_info': [
                'plant', 'plant details', 'generation plant', 'power plant', 'generator info',
                'plant information', 'plant status', 'plant list', 'list of plants',
                'details of generation units', 'generating units', 'generation capacity',
                'power station', 'unit capacity', 'installed capacity', 'plant data',
                'plf', 'paf', 'variable cost', 'aux consumption', 'max power', 'var cost',
                'min power', 'rated capacity', 'type', 'auxiliary consumption', "maximum power",
                "minimum power", "technical minimum", "maximum power", "minimum power", "aux usage", "auxiliary usage"
            ]
        }

        low = raw_text.lower()
        for intent, kws in intents.items():
            if any(k in low for k in kws):
                return intent

        for intent, kws in intents.items():
            if any(tok in toks for toks in [tokens] for tok in kws):
                return intent

        return None
    except Exception as e:
        logger.error(f"Intent detection error: {e}")
        return None

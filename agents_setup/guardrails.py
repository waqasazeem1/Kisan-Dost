from agents import GuardrailFunctionOutput, input_guardrail


@input_guardrail
async def farming_topic_guardrail(ctx, agent, input_text):
    text = str(input_text).lower().strip()

    blocked_keywords = [
        "human medicine", "insaan ki dawai", "meri tabiyat", "mera bukhar",
        "meri health", "doctor ke paas", "chest pain", "headache",
        "sar dard", "blood pressure", "sugar check", "crypto",
        "bitcoin", "politics", "election", "cricket match", "movie recommendation",
    ]

    is_off_topic = any(keyword in text for keyword in blocked_keywords)

    return GuardrailFunctionOutput(
        output_info={"is_off_topic": is_off_topic},
        tripwire_triggered=is_off_topic,
    )
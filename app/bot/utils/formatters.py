def format_result(data: dict) -> str:
    city = data["city"]
    cc = data["country_code"]

    lines = [
        f"🏙 <b>{city}</b> · {cc}",
        "",
    ]

    w = data.get("weather")
    if w:
        lines.append("🌤 <b>Погода</b>")
        lines.append(f"├ {w['description'].capitalize()}")
        lines.append(f"├ <b>{w['temp']:+.1f}°C</b>  (ощущается {w['feels_like']:+.1f}°C)")
        lines.append(f"├ Влажность: {w['humidity']}%")
        lines.append(f"└ Ветер: {w['wind_speed']} м/с")
    else:
        lines.append("🌤 <b>Погода</b>")
        lines.append("└  <i>нет данных</i>")

    lines.append("")

    c = data.get("currency")
    if c:
        if c["from_currency"] == c["to_currency"]:
            lines.append(f"💰 <b>Валюта:</b>  {c['to_currency']}")
            lines.append(f"└  {c['amount']:.0f} {c['to_currency']}")
        else:
            lines.append("💱 <b>Конвертация</b>")
            lines.append(
                f"├ {c['amount']:.0f} {c['from_currency']}  ->  " f"<b>{c['result']:.2f} {c['to_currency']}</b>"
            )
            lines.append(f"└  1 {c['from_currency']} = " f"{c['rate']:.4f} {c['to_currency']}")
    else:
        lines.append("💱 <b>Конвертация</b>")
        lines.append("└ <i>нет данных</i>")

    return "\n".join(lines)

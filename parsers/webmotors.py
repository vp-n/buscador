from urllib.parse import urlparse
import re

def identificar_favicon(link):
    dominio = urlparse(link).hostname or "www.webmotors.com.br"
    return f"https://www.google.com/s2/favicons?domain={dominio}&sz=64"

def formatar_versao_para_url(versao):
    return (
        versao.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("--", "-")
        .replace("º", "")
        .replace("ç", "c")
        .replace(",", "")
        .replace(".", "")
    )

def extrair_combustivel(versao_str):
    """Detecta tipo de combustível a partir da string da versão."""
    versao_str = versao_str.upper()
    if "FLEX" in versao_str:
        return "Flex"
    elif "GASOLINA" in versao_str:
        return "Gasolina"
    elif "ETANOL" in versao_str:
        return "Etanol"
    elif "DIESEL" in versao_str:
        return "Diesel"
    elif "ELÉTRICO" in versao_str or "ELETRICO" in versao_str:
        return "Elétrico"
    elif "HÍBRIDO" in versao_str or "HIBRIDO" in versao_str:
        return "Híbrido"
    else:
        return ""

def extrair_carros_completos_webmotors(dados):
    carros = []
    resultados = dados.get("dom", {}).get("SearchResults", [])

    for item in resultados:
        try:
            spec = item.get("Specification", {})
            seller = item.get("Seller", {})
            media = item.get("Media", {})
            preco = item.get("Prices", {}).get("Price")
            imagens = media.get("Photos", [])
            imagem = None

            if imagens:
                raw_path = imagens[0].get("PhotoPath", "").replace("\\", "/")
                imagem = f"https://image.webmotors.com.br/_fotos/anunciousados/gigante/{raw_path}?s=fill&w=249&h=178&q=70&t=true"

            # Dados para montar o link do anúncio
            marca = spec.get("Make", {}).get("Value", "").lower()
            modelo = spec.get("Model", {}).get("Value", "").lower()
            versao_raw = spec.get("Version", {}).get("Value", "")
            versao_formatada = formatar_versao_para_url(versao_raw)
            unique_id = str(item.get("UniqueId", ""))
            ano_modelo = str(int(spec.get("YearModel", 0))) if spec.get("YearModel") else ""
            ano_fabricacao = str(spec.get("YearFabrication", "")) or ano_modelo
            portas = f"{spec.get('NumberPorts', '')}-portas"
            listing_type = item.get("ListingType")

            link = None
            if listing_type in ["U", "N"]:
                link = f"https://www.webmotors.com.br/comprar/{marca}/{modelo}/{versao_formatada}/{portas}/{ano_fabricacao}-{ano_modelo}/{unique_id}"

            # Combustível dinâmico
            combustivel = extrair_combustivel(versao_raw)

            carros.append({
                "marca": marca.upper(),
                "modelo": modelo.upper(),
                "ano": int(spec.get("YearModel", 0)) if spec.get("YearModel") else None,
                "cambio": spec.get("Transmission") or "",
                "descricao": spec.get("Title") or "",
                "preco": preco,
                "quilometragem": int(spec.get("Odometer", 0)) if spec.get("Odometer") else None,
                "combustivel": combustivel,
                "localizacao": seller.get("City", "") or seller.get("State", ""),
                "imagem": imagem,
                "link": link,
                "site_icon": identificar_favicon(link)
            })

        except Exception as e:
            print(f"[ERRO] Falha ao processar item: {e}")
            continue

    return carros

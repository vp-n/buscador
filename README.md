# buscador

buscadordecarro/
│
├── crawlers/
│   ├── olx.py
│   ├── icarros.py
│   ├── webmotors.py
│   ├── meu_carro_novo.py
│   ├── mobauto.py
│   ├── napista.py
│   ├── autoavaliar.py
│   ├── facebook.py
│   ├── repassafacil.py
│   ├── estacarro.py
│   ├── volat.py
│   └── vapt.py
│
├── main.py
├── utils/              # Funções auxiliares (ex: limpeza de dados, logging)
│   └── helpers.py
├── requirements.txt
└── README.md


## 📘 Documentação da Rota `/get-dom`

### 🔗 Endpoint:

```
GET /get-dom
```

### 📌 Parâmetros comuns:

| Parâmetro | Obrigatório | Descrição                                                   |
| --------- | ----------- | ----------------------------------------------------------- |
| `site`    | ✅           | Nome do site (ex: `olx`)                                    |
| `estado`  | ✅           | Sigla do estado (ex: `sp`)                                  |
| `carro`   | ✅           | Modelo ou nome do carro                                     |
| `marca`   | ⚠️ Alguns   | Marca do carro (ex: `fiat`) – usado no Webmotors e Mobiauto |

---

## 🟢 Exemplos por Site

### 🔹 OLX

```
/get-dom?site=olx&estado=sp&carro=kwid
```

### 🔹 iCarros

```
/get-dom?site=icarros&estado=mg&carro=uno
```

### 🔹 Mobiauto

```
/get-dom?site=mobiauto&estado=sp&marca=chevrolet&carro=onix
```

### 🔹 Webmotors

```
/get-dom?site=webmotors&estado=rj&marca=fiat&carro=uno
```

### 🔹 NaPista

> Não precisa do estado, apenas do modelo do carro.

```
    /get-dom?site=napista&carro=gol
```

### 🔹 Facebook Marketplace

```
/get-dom?site=facebook&estado=sp&carro=civic
```

---

### ❗ Observações:

* Os nomes dos sites devem estar em **minúsculo** (ex: `webmotors`, `facebook`).
* O parâmetro `marca` só é obrigatório para os sites: `webmotors` e `mobiauto`.
* O `estado` deve estar no formato de sigla: `sp`, `rj`, `am` etc.
* A cidade é automaticamente derivada da sigla do estado nos crawlers.

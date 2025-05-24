# 🤖 LLM Hallucination & Robustness Detector (Single & Batch Mode)

[![Streamlit](https://img.shields.io/badge/Streamlit-App-green)](https://share.streamlit.io/epaunova/llm-hallucination-detector/main/hallucination_app.py)

## Описание

Това е интерактивно Streamlit приложение за оценка на изходите от големи езикови модели (LLMs).  
Поддържа както единичен анализ на един output, така и batch режим за множество outputs наведнъж.

### Основни функции:

- **Откриване и визуализация на потенциални hallucination patterns** чрез подчертани trigger фрази  
- **Ръчна оценка на factuality** чрез плъзгач (slider)  
- **Автоматична (симулирана) LLM оценка** с бутон за бърза диагностика  
- **Токсичност** – проверка за токсични и обидни думи  
- **Бар графика с честота на hallucination фразите**  
- **Batch режим** за обработка и анализ на множество outputs наведнъж  
- Статистика и разпределение на тригерите и токсичността в batch  

---

## Как да използваш

1. **Single mode (по подразбиране)**  
   - Постави един output в полето "LLM Output".  
   - Виж подчертани hallucination triggers, направи ръчна оценка и пусни авто проверка.  
   - Виж токсичността и бар графика с тригерите.  

2. **Batch mode**  
   - Отметни "Batch mode" чекбокса.  
   - Постави няколко output-а, разделени с три тирета (`---`).  
   - Прави ръчни оценки за всеки output отделно.  
   - Виж обща статистика, броя токсични и hallucination outputs.  
   - Графика с честотата на всички hallucination тригери в batch.  

---

## Инсталация

```bash
pip install streamlit pandas

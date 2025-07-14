import gradio as gr
import pandas as pd
import io
from langchain_community.llms import Ollama  # 올바른 import

class ExcelChatBot:
    def __init__(self):
        # Ollama LLM 초기화 (모델명은 상황에 맞게 수정)
        self.llm = Ollama(model="gemma2:9b", temperature=0)

    def _summarize_excel(self, excel_file: io.BytesIO) -> str:
        try:
            df = pd.read_excel(excel_file)
            summary = (
                f"엑셀 데이터 요약:\n"
                f"- 컬럼명: {', '.join(df.columns)}\n"
                f"- 데이터 샘플:\n{df.head(3).to_string(index=False)}"
            )
            return summary
        except Exception as e:
            return f"엑셀 파일을 처리하는 중 오류가 발생했습니다: {e}"

    def _create_prompt(self, question: str, excel_summary: str | None) -> str:
        prompt = "당신은 엑셀 함수 및 데이터 분석에 능한 한국어 AI 비서입니다.\n"
        if excel_summary:
            prompt += excel_summary + "\n"
        prompt += f"사용자의 질문에 대해 명확하고 친절하게 답변해주세요.\n질문: {question}\n답변:"
        return prompt

    def answer(self, question: str, excel_file: io.BytesIO | None) -> str:
        # 엑셀 요약 생성
        excel_summary = None
        if excel_file is not None:
            excel_summary = self._summarize_excel(excel_file)

        prompt = self._create_prompt(question, excel_summary)

        # Ollama LLM 호출
        try:
            response = self.llm.generate([prompt])  # 리스트로 감싸기
            return response.generations[0][0].text.strip()
        except Exception as e:
            return f"⚠️ 답변 생성 중 오류가 발생했습니다: {e}"

# Gradio UI 구성
def gr_interface(question, excel_file):
    chatbot = ExcelChatBot()
    return chatbot.answer(question, excel_file)

with gr.Blocks() as demo:
    gr.Markdown("# 엑셀 질문 챗봇")
    question_input = gr.Textbox(label="질문을 입력하세요")
    excel_input = gr.File(label="엑셀 파일 업로드 (선택 사항)", file_types=[".xlsx", ".xls"])
    answer_output = gr.Textbox(label="답변", lines=10)

    submit_btn = gr.Button("질문하기")

    submit_btn.click(
        fn=gr_interface,
        inputs=[question_input, excel_input],
        outputs=answer_output
    )

demo.launch()
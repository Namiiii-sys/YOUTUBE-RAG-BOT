# raw_answer = main_chain.invoke(question)

#           # Split on newlines and strip empty lines
#             lines = [line.strip() for line in raw_answer.split('\n') if line.strip()]

#           # Add numbering
#             numbered = [f"{i+1}. {line.lstrip('- ').strip()}" for i, line in enumerate(lines)]

#           # Join again
#             answer = "\n".join(numbered)
            
#             print("[DEBUG] Final answer:", answer)
import streamlit as st
from together import Together
key = 'f50c14c49fa7f5dbd037986bf1c3955b688ca9af426e5cea861108f2008d9506'
client = Together(api_key=key)

# Streamlit başlık
st.title("Telefon Numarası Temizleme")

# Kullanıcıdan telefon numarası al
phone_number = st.text_input("Telefon numarasını girin:", "")

# Temizlenmiş telefon numarasını gösterecek alan
if st.button("Numarayı Temizle"):
    if phone_number.strip():  # Eğer kullanıcı bir numara girdiyse
        prompt_y = f"""

        Return **only** the final cleaned phone number after processing. Do not include explanations, additional text, or formatting. The response must be the final number or `NULL`.
    
        **1. Clear**
        Remove any characters that are not digits. Keep only numeric digits (0-9)
    
        **2. Delete the Area Code**  
        Remove prefixes like '90', '+90', '900', '0', '090', or '0090'.

        **3. Meaningful Check First Step**
        Check if the number matches the format 5XXXXXXXXX
        - If yes, proceed to the next step.
        - If no, return "NULL".

        **4. Measure Length**  
        - If the resulting number is less than 10 digits, return "NULL".  
        - If it is exactly 10 digits, proceed to the next step.

        **5. Handling Extra Digits**  
        Check if the number exceeds 10 digits.  
        - If it does, keep only the first 10 digits and ignore the rest.  
        - Otherwise, proceed to the next step.
    
        **6. Format Match**  
        Check if the number matches the format 5XXXXXXXXX (10 digits starting with 5).  
        - If yes, proceed to the next step.  
        - If no, return "NULL".

        **7. Meaningful Check Second Step**  
        Validate the number for uniqueness and meaningfulness:  
        - If it is a repetitive or sequential pattern, return "NULL".  
        - Otherwise, return the cleaned number.

        Process this number: "{phone_number}"
        """
        
        # API çağrısı
        try:
            response = client.chat.completions.create(
                model="Qwen/QwQ-32B-Preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Return only the cleaned phone number, following the steps strictly. Make all processing must be invisible in the background, just give the final output."},
                    {"role": "user", "content": prompt_y},
                ],
                max_tokens=None,
                temperature=0.0,
                top_p=0.1,
                top_k=1,
                n=1,
                seed=42,
                repetition_penalty=1,
                stream=True
            )
            # API yanıtı okuma
            cleaned_number = ""
            for token in response:
                if hasattr(token, 'choices'):
                    cleaned_number += token.choices[0].delta.content
            
            # Temizlenmiş numarayı göster
            st.success(f"{cleaned_number}")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen bir telefon numarası girin!")

# Görseli küçük şekilde sağ alt köşede göster
st.markdown(
    """
    <style>
    .small-image-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 150px;  /* Küçük boyut için genişlik */
        height: auto;
        cursor: pointer;
    </style>
    """,
    unsafe_allow_html=True,
)

# Görselin tam ekran versiyonu
with st.expander("LLM Diagram", expanded=False):  # Varsayılan olarak gizli
    st.image("llmdiagram.png", use_container_width=True, caption="LLM Diagram")

# Küçük görsel
st.markdown(
    f"""
    <a href="#" onclick="document.querySelector('.streamlit-expander').click();">
        <img src="llmdiagram.png" class="small-image-container"/>
    </a>
    """,
    unsafe_allow_html=True,
)
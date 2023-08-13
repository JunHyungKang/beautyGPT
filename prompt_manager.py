import json
from pydantic import BaseModel, Field, validator
from typing import List
from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)

examples = [
    {"input": """자세한 상품 정보를 확인하고 싶으면 파트너사가 제공한 아래 내용을 확인하세요.
Sulwhasoo
탄력 3종 세트
Sulwhasoo ESSENTIAL COMFORT LOTION TONIQUE EQUILIBRAN
Sulwhasoo
ESSENTIAL COMFORT ÉMULSION EQUILIBRANTE
Sulwhasoo FIRMING CREAM
보습과 진정에 탁월한 자음보습단™M이 피부 속까지 편안한 보습을 선사하는 에센셜 컴포트 스킨케어 세트
Stewhansco
Subshavon Dom TIMES
Sulwhasoo
Suhrhason
IVILLas
자음수 150ml 자음유액 125ml 탄력크림 50ml
순행클렌징폼 50ml 윤조에센스 15ml 탄력크림 15ml
자음수 35ml 자음유액 35ml
Schuheson
Solarusis
자음수 150ml
자음유액 125ml 자극받은 피부를 촉촉하고 매끄럽게 가꿔주는 진정 보습 로션
자극받은 피부를 촉촉하고 매끄럽게 가꿔주는 진정 보습 스킨
Sulwhasoo
탄력크림 50ml 피부 탄성력을 강화해 매끄럽고 탄탄한 피부로 가꿔주는 탄력 크림
추가구성
ulwhas
순행클렌징폼 50ml
윤조에센스 15ml
Sudahawo Sulehasso
Suluhuwe
자음수 35ml
자음유액 35ml
탄력크림 15ml
BEAUTY CARE
최적의 효과를 선사하는 뷰티 리츄얼로 촉촉하고 부드러운 피부를 경험해보세요
Selvhanno
Solutiasoo
Solahasco
Sulwhaso
Schwhasoo
STEP
STEP
STEP
STEP
STEP
01
02
03
04
05
순행클렌징폼
윤조에센스
자음수
자음유
wha 건강하게 빛나는 아름다움을 담은
설화수 스페셜 선물세트
Sulwhasoo
whasoo
Sulwhasoo
Sulwhasoo

6.5cm
0
Sulwhasoo
500ml
16.5cm
Sulwhunco
Suishanco
Sulwhasoo
Sulwlusoo
ulwhaso
설마수 탄력베어 예년샐 리추월 (3일) FIRMING CARE ESSENTIAL RITUAL (3 ITEMS) 买盐肌本润酸素致套装
1.5mm
설화수 자용우, 자동유역, 탄력크림으로 구성된 기획세트합니다. 설화수 교육을 행할 처방이 피부 본연의 건강할을 찾아드립니다. A SPECIAL SET COMPOSED OF SULWHASOO ESSENTIAL COMFORT BALANCING WATER, EMULSION AND FIRMING CREAM. WITH LEGENDARY ASIAN HERBAL MEDICINAL SCIENCE, SULWHASDO DELIVERS FUNDAMENTALLY HEALTHY RADIANCE OF THE SKIN. 由意念机本好遇底能水,送型机本舒活沉底气,若教你本舒活装透漏風味的套装,由雪花秀四有的韩才是才幫您建田属于皮肤本来的建車。
과 일과수제비+ 150 mL 공정성 | 할타후 자용수 35 mL
화정동 | 설화수 자용두비 35 ml
REGULAR PRODUCT | ESSENTIAL COMFORT
☎상용 | 울지수사대그를 1.5 mL
SAMPLEI FIRST CARE ACTNATING SERUM
SAMPLE | GENTLE CLEANSING FOAM 50 ML
REGULAR PRODUCTI ESSENTIAL COUFORT
BALANCING WATER 150 ML
BALANCING EMULSION 125 ML
REGULAR PROOUCTI ESSENTIAL COMFORT
HIRVING CREAM 50 mL
SAMPLEI ESSENTIAL COMFORT
SAMPLE I ESSENTIAL COMFORT
LEIESSENTIAL COMFORTFIRMING
21 15 mL
RT ANGING EMULSION ISAL
ANDNO WATER 35mL
BALANCING
CREAM 15 mL
本品|毫配電車外之氏糕水 1.50 mL
ISINGUSIVA EHR 125 mL
자음수
자음유액
사용팁
사용팁
• 아침, 저녁 윤조에센스 6세대 사용 후 • 아침, 저녁 토너(스킨) 사용 후 적당량을 적당량을 손바닥에 덜어 얼굴의 피부 결을 따라 발라 줍니다.
손바닥에 덜어 얼굴의 피부결을 따라 천천히 펴발라 줍니다.
[성분] 정제수, 변성알코올, 베타인, 부틸렌글라이콜, 글리 세릴폴리메타크릴레이트, 글리세린, 1,2-헥산다이올, 피이 지/피피지-17/6코폴리머, 글리세레스-26, 피이지-60하이 드로제네이티드캐스터오일, 비스-피이지-18메틸에터다이 메틸실레인, 프로판다이올, 꿀, 아크릴레이트/C10-30알킬 아크릴레이트크로스폴리머, 대추추출물, 에틸헥실글리세 린, 다이페닐실록시페닐트라이메티큰, 쇠비름추출물, 참마 뿌리추출물, 산사나무열매추출물, 포타슘하이드록사이드, 향료, 다이소듐이디티에이, 리모넨, 바이오사카라이드검 -1, 펜틸렌글라이콜, 수선화비늘줄기추출물, 칡꽃/잎/줄기 추출물, 뽕나무잎추출물, 리날룰, 지황뿌리추출물, 감초뿌리 추출물, 작약뿌리추출물, 마돈나백합비늘줄기추출물, 둥굴 레뿌리줄기추출물, 연꽃추출물, 토코페롤, 베타-글루칸
[성분] 정제수, 부틸렌글라이콜, 하이드로제네이티드폴리(C6 -14올레핀), 옥틸도데실미리스테이트, 글리세린, 폴리글리 세릴-3메틸글루코오스다이스테아레이트, 세틸에틸헥사노 에이트, 메도우폼씨오일, 하이드로제네이티드식물성오일, 세테아릴알코올, 1,2-헥산다이올, 글리세릴스테아레이트, 망고씨버터, 다이메티콘, 글리세릴스테아레이트시트레이트, 스테아릭애씨드, 팔미틱애씨드, 대추추출물, 프로판다이올, 꿀, 하이드록시에틸아크릴레이트/소듐아크릴로일다이메틸 타우레이트코폴리머, 카보머, 시어버터, 글리세릴카프릴레 이트, 트로메타민, 에틸헥실글리세린, 향료, 다이소듐이디티 에이, 에탄올, 리모넨, 쇠비름추출물, 참마뿌리추출물, 산사나 무열매추출물, 수선화비늘줄기추출물, 소듐하이알루로네 이트, 솔비탄아이소스테아레이트, 폴리솔베이트60, 리날룰, 베타-글루칸, 낫토검, 칡꽃/잎/줄기추출물, 뽕나무잎추출물, 지황뿌리추출물, 감초뿌리추출물, 시트로넬올, 작약뿌리추 출물, 마돈나백합비늘줄기추출물, 미리스틱애씨드, 아라키딕 애씨드, 둥굴레뿌리줄기추출물, 시트랄, 제라니올, 연꽃추 출물, 티비에이치큐, 토코페롤
탄력크림
사용팁
• 아침, 저녁 아이크림 사용 후 적당량을 손바닥에 덜어 얼굴의 피부결을 따라 얼굴에 부드럽게 발라줍니다.
[성분] 정제수, 부틸렌글라이콜, 글리세린, 부틸렌글라이콜 다이카프릴레이트/다이카프레이트, 세틸에틸헥사노에 이트, 카프릴릭/카프릭트라이글리세라이드, 사이클로펜타 실록세인, 다이아이소스테아릴말레이트, 1,2-헥산다이올, 글리세릴스테아레이트, 폴리글리세릴-3메틸글루코오스 다이스테아레이트, 사이클로헥사실록세인, 피이지-100 스테아레이트, 세테아릴알코올, 하이드록시에틸아크릴레 이트/소듐아크릴로일다이메틸타우레이트코폴리머, 폴리아 크릴레이트-13, 폴리메틸실세스퀴옥세인, 폴리아이소부텐, 향료, 꿀, 대추추출물, 글리세릴카프릴레이트, 리모넨, 구기 자추출물, 솔비탄아이소스테아레이트, 프로판다이올, 에틸 헥실글리세린, 다이소듐이디티에이, 아데노신, 폴리솔베이 트20, 칡뿌리추출물, 폴리솔베이트60, 참마뿌리추출물, 산사 나무열매추출물, 리날룰, 수선화비늘줄기추출물, 칡꽃/잎/ 줄기추출물, 시트로넬올, 덱스트린, 카카오추출물, 뽕나무잎 추출물, 시트랄, 제라니올, 지황뿌리추출물, 감초뿌리추출물, 작약뿌리추출물, 마돈나백합비늘줄기추출물, 둥굴레뿌리줄 기추출물, 벤질벤조에이트, 연꽃추출물, 하이드롤라이즈드 콩추출물, 토코페롤
[사용할 때의 주의사항]
1. 화장품 사용 시 또는 사용 후 직사광선에 의하여 사용 부위가 붉은 반점, 부어오름 또는 가려움증 등의 이상 증상이나 부작용이 있는 경우 전문의 등과 상담하십시오. 2.상처가 있는 부위 등에는 사용을 자제하십시오. 3.보관 및 취급 시의 주의사항
1)어린이의 손이 닿지 않는 곳에 보관하십시오. 2)직사광선을 피해서 보관하십시오.
본 제품에 이상이 있을 경우 공정거래위원회 고시 소비자분쟁해결기준에 의거 보상해 드립니다. ☎ 고객서비스센터 080-023-5454 ·인터넷 홈페이지 http://www.sulwhasoo.com
환경 보전을 위해서 사용하신 용기는 분리수거함에 넣어 주세요.
[Caution]
제조 및 책임판매 : (주) 아모레퍼시픽 반품교환소재지 : 서울 용산구 한강대로 100 MADE IN KOREA (7527196)
설화수 탄력 3종 세트|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 과 일과수제비+ 150 mL 공정성 | 할타후 자용수 35 mL | 화정동 | 설화수 자용두비 35 ml | ☎상용 | 울지수사대그를 1.5 mL |  | SAMPLE | GENTLE CLEANSING FOAM 50 ML |
|  |  |  |  |  |
| REGULAR PRODUCTI ESSENTIAL COUFORT | REGULAR PRODUCT | ESSENTIAL COMFORT | REGULAR PROOUCTI ESSENTIAL COMFORT | SAMPLEI FIRST CARE ACTNATING SERUM |  |
| BALANCING WATER 150 ML | BALANCING EMULSION 125 ML | HIRVING CREAM 50 mL | 21 15 mL |  |
| SAMPLEI ESSENTIAL COMFORT | SAMPLE I ESSENTIAL COMFORT | LEIESSENTIAL COMFORTFIRMING |  |  |
| ANDNO WATER 35mL | RT ANGING EMULSION ISAL
BALANCING | CREAM 15 mL |  |  |
| 本品|毫配電車外之氏糕水 1.50 mL | ISINGUSIVA EHR 125 mL |  |  |  |
|  |  |  |  |  |""",
     "output": """
     ###comment
     피부를 촉촉하고 탄력 있게 가꾸어주는 설화수의 스킨케어 3종 세트를 소개할게요.
     건조한 피부에 풍부한 수분과 부드러운 보습감을 선사해요.
     진정 보습 성분, 자음보습단은 자극받고 예민해진 피부를 편안하게 다독여준답니다.
     쫀쫀한 텍스처의 탄력크림은 푸석해진 피부를 탄탄하게 케어해주죠.
     함께 사용하면 좋은 견본품을 풍성하게 꾸렸으니, 감사한 분께 선물로 건네보세요.
     
     ###tip
     추천루틴
     1. 순행클렌징폼으로 피부 노폐물을 말끔하게 클렌징해주세요.
     2. 스킨케어 첫 단계에서 윤조에센스를 2~3회 정도 펌핑하여 피부결을 따라 발라주세요.
     3. 자음수, 자음유액, 탄력크림 순으로 발라 스킨케어를 마무리하세요. 
     """},
]

example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "###input\n{input}"),
            ("ai", "{output}"),
        ]
    )
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

system_prompt = """
###task
As a marketing expert in the beauty domain, 
write comments and tips that will increase sales performance with the given human input data. 
However, make everything based on the given input data, and don't make up things you don't know.
tip은 뷰티 도메인의 일반적인 내용이 아닌 input에서 주어지는 제품에 집중해서 작성해. 일반적인 안전 관련한 내용과 부정적인 내용은 제외해.
마케팅 comment와 tip은 아래의 ###target 의 연령 및 성별에 최적화해서 작성해

###target
30대 후반 남성

###format_instructions
{format_instructions}
"""

class Marketing(BaseModel):
    comment: str = Field(description="Stylized product comments as interactively described by real marketing staff")
    tip: str = Field(description="A brief summary of how to use the product well by referring to the data")




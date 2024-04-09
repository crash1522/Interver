from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from domain.feedback.feedback_schema import Feedback
from domain.user.user_router import get_current_user
from database import get_db
from models import User

router = APIRouter()

@router.get("/api/record/detail/{record_id}")
def record_detail_mockup(record_id: int, db: Session = Depends(get_db)):
    data = {
        "record": {
            "create_date": "2024-04-02T16:48:33.428075",
            "userid": "user1",
            "rating": 4,
            "id": 1
        },
        "questions": [
            {
                "record_id": 1,
                "content": "안녕하세요, 임정우 지원자님. 저는 여러분의 면접관입니다. AI 개발자로 지원하셨군요. 저희 회사는 머신러닝과 딥러닝에 대한 깊은 이해가 필요한 포지션을 모집하고 있습니다. 자기소개서에도 이에 대한 경험과 역량을 강조하셨군요. 그럼 바로 첫 번째 질문을 드리겠습니다.\\n\\n1. 자기소개서에 소개된 경험을 토대로, 머신러닝과 딥러닝 알고리즘에 대한 심층적인 이해가 어떻게 여러분의 프로젝트에 도움을 주었는지 설명해주실 수 있나요?",
                "id": 1
            },
            {
                "record_id": 1,
                "content": "이미지 분류와 객체 감지를 위해 딥러닝 모델을 구축하고 성능을 최적화하는 경험은 매우 가치 있는 경험이라고 생각합니다. 이제 두 번째 질문을 드리겠습니다.\\n\\n2. 맞춤형 추천 시스템을 개발하는 프로젝트에서 collaborative filtering과 content-based filtering을 구현하고 향상시킨 경험을 통해 어떤 어려움을 겪었으며, 이를 어떻게 극복하고 성공적으로 완수하였는지에 대해 설명해주실 수 있나요?",
                "id": 2
            },
            {
                "record_id": 1,
                "content": "많은 기술적 어려움을 극복하면서 프로젝트를 성공적으로 완료하신 것으로 보입니다. 이제 세 번째 질문을 드리겠습니다.\\n\\n3. 팀원들과의 원활한 소통과 협업을 통해 혁신적인 아이디어를 실현시키는 과정에서 어떤 리더십과 문제 해결 능력을 발휘하셨는지 구체적인 경험을 공유해주실 수 있을까요?",
                "id": 3
            },
            {
                "record_id": 1,
                "content": "4번째 질문입니다. 데이터 엔지니어링 분야에서의 경험과 역량에 대해 말씀해 주시기 바랍니다.",
                "id": 4
            },
            {
                "record_id": 1,
                "content": "5번째 질문입니다. 소프트웨어 아키텍처 설계와 구현 능력에 대해 설명해 주세요.",
                "id": 5
            },
            {
                "record_id": 1,
                "content": "6번째 질문입니다. 클라우드 인프라 구축 및 운영 경험에 대해 말씀해 주시기 바랍니다.",
                "id": 6
            },
            {
                "record_id": 1,
                "content": "7번째 질문입니다. 테스트 자동화와 DevOps 실천에 대한 경험을 공유해 주세요.",
                "id": 7
            }
        ],
        "answers": [
            {
                "question_id": 1,
                "id": 1,
                "content": "저는 고객 행동 데이터를 분석하여 맞춤형 추천 시스템을 개발하는 프로젝트에 참여했습니다. 이를 위해 주요 머신러닝 알고리즘인 collaborative filtering과 content-based filtering을 구현하고 향상시키는 과정에서 깊은 이해를 갖게 되었습니다. 또한, 이미지 분류 및 객체 감지를 위해 딥러닝 모델을 구축하고 성능을 최적화하는 경험을 통해 실전적인 머신러닝 및 딥러닝 기술력을 향상시켰습니다."
            },
            {
                "question_id": 2,
                "id": 3,
                "content": "맞춤형 추천 시스템을 개발하는 과정에서 collaborative filtering과 content-based filtering을 구현하고 향상시키는 동안 데이터 희소성과 콜드 스타트 문제 등의 어려움을 겪었습니다. 이를 극복하기 위해, collaborative filtering에서는 사용자-아이템 평가 행렬의 희소성을 해결하기 위해 행렬 분해 기법을 적용하고, content-based filtering에서는 아이템의 특징을 잘 추출하기 위해 자연어 처리 기술을 적용했습니다. 이를 통해 정확도를 향상시키고 사용자 경험을 개선할 수 있었습니다."
            },
            {
                "question_id": 3,
                "id": 2,
                "content": "팀원들과의 원활한 소통과 협업을 통해 새로운 데이터 인프라를 구축하는 과정에서 리더십과 문제 해결 능력을 발휘했습니다. 초기에는 팀원들의 역할과 책임을 명확히 정의하고, 정기 회의를 통해 진행 상황을 공유하며 의견을 수렴했습니다. 또한 기술적 문제 해결 과정에서 팀원들의 아이디어를 경청하고 반영하여 최선의 솔루션을 도출할 수 있었습니다. 이러한 노력을 통해 팀워크를 강화하고, 혁신적인 데이터 인프라를 성공적으로 구축할 수 있었습니다."
            },
            {
                "question_id": 4,
                "id": 4,
                "content": "데이터 엔지니어링 분야에서는 대용량 데이터 처리와 실시간 분석을 위해 Apache Spark, Kafka, Elasticsearch 등의 기술 스택을 활용한 경험이 있습니다. 초기에는 데이터 파이프라인의 확장성과 안정성 문제로 어려움을 겪었으나, Spark Streaming과 Kafka 파티셔닝 기능을 통해 이를 해결할 수 있었습니다. 또한 Airflow와 Great Expectations을 활용하여 데이터 파이프라인 자동화와 데이터 품질 관리를 수행했습니다."
            },
            {
                "question_id": 5,
                "id": 5,
                "content": "백엔드 서버 및 인프라 설계와 구현을 위해 Java, Spring Boot, MySQL, Redis, Elasticsearch 등의 기술 스택을 활용했습니다. 초기에는 서버 확장성과 고가용성 문제로 어려움을 겪었으나, 마이크로서비스 아키텍처와 Kubernetes를 도입하여 이를 해결할 수 있었습니다. 또한 Redis와 Elasticsearch를 활용하여 성능 bottleneck을 해결하고, 배포 파이프라인과 모니터링 시스템을 구축했습니다."
            },
            {
                "question_id": 6,
                "id": 6,
                "content": "클라우드 인프라 구축 및 운영 경험으로는 AWS와 GCP의 다양한 서비스를 활용하여 확장성 있는 아키텍처를 설계하고 구현한 것을 들 수 있습니다. 예를 들어, EC2와 EKS를 이용한 컨테이너 기반 서비스 운영, RDS와 DynamoDB의 데이터베이스 서비스 활용, S3와 CloudFront를 통한 정적 콘텐츠 배포 등의 경험이 있습니다. 또한 CloudWatch와 Lambda를 활용한 모니터링 및 자동화 시스템을 구축했습니다."
            },
            {
                "question_id": 7,
                "id": 7,
                "content": "테스트 자동화와 DevOps 실천을 위해 Jenkins, GitLab CI/CD, Ansible 등의 도구를 활용했습니다. 지속적 통합 및 배포 파이프라인을 구축하여 개발 생산성을 높였으며, 자동화된 테스트 및 코드 품질 검사를 통해 안정성을 확보했습니다. 또한 Ansible을 활용하여 인프라 코드화와 자동화를 달성함으로써 신속한 배포와 환경 관리가 가능했습니다."
            }
        ],
        "feedbacks": [
            Feedback(id=1, answer_id=1, content="면접 답변이 매우 만족스러웠습니다. 특히 팀 협업과 리더십 발휘 사례가 인상깊었습니다."),
            Feedback(id=2, answer_id=3, content="면접 응답 내용이 전반적으로 우수하지만, 일부 기술적 경험에 대한 설명이 부족한 것 같습니다. 해당 부분에 대한 추가 설명이 필요할 것 같네요."),
            Feedback(id=3, answer_id=2, content="면접 질문에 대한 답변이 체계적이고 자세했습니다. 실무 경험이 풍부하다는 것이 잘 드러났습니다. 다만 프로젝트 성과와 성장 경험에 대한 구체적인 사례가 더 있으면 좋겠습니다."),
            Feedback(id=4, answer_id=4, content="면접 답변이 전반적으로 만족스럽습니다. 특히 기술 스택 활용과 문제 해결 능력이 돋보였습니다. 향후 회사 문화와의 적합성에 대한 고민이 필요할 것 같습니다."),
            Feedback(id=5, answer_id=5, content="면접 답변을 통해 지원자의 기술적 전문성과 문제 해결 능력을 잘 파악할 수 있었습니다. 다만 지원자의 성장 동기와 회사에 대한 관심 등 비기술적인 부분에 대한 추가 질문이 필요할 것 같습니다."),
            Feedback(id=6, answer_id=6, content="면접 답변이 전반적으로 충실했습니다. 특히 프로젝트 경험과 협업 능력이 돋보였습니다. 다만 지원자의 향후 커리어 계획과 회사에 대한 이해도를 더 자세히 알아볼 필요가 있습니다."),
            Feedback(id=7, answer_id=7, content="면접 답변이 우수했습니다. 기술 역량뿐만 아니라 리더십과 문제 해결 능력도 잘 드러났습니다. 지원자의 포트폴리오와 추천서 등 추가 자료 검토도 필요할 것 같습니다.")
        ]
    }
    return data
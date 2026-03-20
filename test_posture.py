import asyncio
import sys
sys.path.insert(0, '.')

from src.services.posture_service import get_aliyun_posture_service, PostureQuantification

async def test_posture_service():
    print("=" * 60)
    print("坐姿检测服务测试")
    print("=" * 60)
    
    service = get_aliyun_posture_service()
    
    print(f"\n服务状态: {'可用' if service.is_available else '不可用（使用模拟数据）'}")
    print(f"Access Key ID: {service.access_key_id[:10]}..." if service.access_key_id else "未配置")
    
    quantification = PostureQuantification()
    
    print("\n" + "-" * 40)
    print("测试量化算法")
    print("-" * 40)
    
    test_cases = [
        {"head_angle": 5, "shoulder_score": 95, "back_score": 90, "eye_distance": 45, "desc": "良好坐姿"},
        {"head_angle": 15, "shoulder_score": 75, "back_score": 80, "eye_distance": 35, "desc": "需注意"},
        {"head_angle": 30, "shoulder_score": 40, "back_score": 50, "eye_distance": 25, "desc": "需纠正"},
    ]
    
    for case in test_cases:
        score = quantification.calculate_posture_score(
            case["head_angle"],
            case["shoulder_score"],
            case["back_score"],
            case["eye_distance"]
        )
        status = quantification.determine_status(score)
        recommendation = quantification.get_recommendation(status, {
            "head_angle": case["head_angle"],
            "shoulder_balance": "良好" if case["shoulder_score"] >= 90 else ("需注意" if case["shoulder_score"] >= 70 else "不平衡"),
            "back_curve": "正常" if case["back_score"] >= 90 else ("轻微弯曲" if case["back_score"] >= 70 else "过度弯曲"),
            "eye_distance": case["eye_distance"]
        })
        
        print(f"\n测试场景: {case['desc']}")
        print(f"  头部角度: {case['head_angle']}°")
        print(f"  肩部评分: {case['shoulder_score']}")
        print(f"  背部评分: {case['back_score']}")
        print(f"  眼睛距离: {case['eye_distance']}cm")
        print(f"  -> 综合评分: {score}")
        print(f"  -> 状态: {status}")
        print(f"  -> 建议: {recommendation}")
    
    print("\n" + "-" * 40)
    print("测试模拟数据生成")
    print("-" * 40)
    
    for i in range(3):
        result = service._get_mock_result()
        print(f"\n模拟测试 {i+1}:")
        print(f"  状态: {result.status}")
        print(f"  评分: {result.score}")
        print(f"  头部角度: {result.head_angle}°")
        print(f"  肩部平衡: {result.shoulder_balance}")
        print(f"  背部弯曲: {result.back_curve}")
        print(f"  眼睛距离: {result.eye_distance}cm")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    print("\n注意：要使用真实的阿里云API进行坐姿检测，需要：")
    print("1. 确保.env文件中配置了正确的阿里云AccessKey")
    print("2. 确保已开通阿里云视觉智能开放平台的动作识别API")
    print("3. 上传至少2张包含人体姿态的图片进行检测")

if __name__ == "__main__":
    asyncio.run(test_posture_service())

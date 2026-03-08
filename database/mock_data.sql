-- ============================================
-- 基于大语言模型的医疗智能体系统 - 模拟数据脚本
-- 说明：此脚本用于插入测试数据，便于开发和测试
-- ============================================

USE medical_ai;

-- ============================================
-- 1. 用户管理模块数据
-- ============================================

-- 1.1 插入角色数据
INSERT INTO roles (role_name, description, status, created_at, updated_at) VALUES
('admin', '系统管理员', 1, NOW(), NOW()),
('doctor', '医生', 1, NOW(), NOW()),
('user', '普通用户', 1, NOW(), NOW()),
('reviewer', '审核员', 1, NOW(), NOW());

-- 1.2 插入权限数据
INSERT INTO permissions (permission_name, resource, action, description, created_at) VALUES
('user:create', 'user', 'create', '创建用户', NOW()),
('user:read', 'user', 'read', '查看用户', NOW()),
('user:update', 'user', 'update', '更新用户', NOW()),
('user:delete', 'user', 'delete', '删除用户', NOW()),
('consultation:create', 'consultation', 'create', '创建问诊', NOW()),
('consultation:read', 'consultation', 'read', '查看问诊', NOW()),
('consultation:review', 'consultation', 'review', '审核问诊', NOW()),
('article:create', 'article', 'create', '创建文章', NOW()),
('article:read', 'article', 'read', '查看文章', NOW()),
('article:update', 'article', 'update', '更新文章', NOW()),
('article:delete', 'article', 'delete', '删除文章', NOW()),
('article:review', 'article', 'review', '审核文章', NOW()),
('system:config', 'system', 'config', '系统配置', NOW()),
('system:log', 'system', 'log', '查看日志', NOW());

-- 1.3 插入用户数据（密码哈希值示例，实际应使用bcrypt等加密）
INSERT INTO users (username, phone, email, password_hash, avatar_url, status, created_at, updated_at) VALUES
('admin', '13800000001', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('doctor1', '13800000002', 'doctor1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('doctor2', '13800000003', 'doctor2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user1', '13800000004', 'user1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user2', '13800000005', 'user2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user3', '13800000006', 'user3@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('reviewer1', '13800000007', 'reviewer1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user4', '13800000008', 'user4@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user5', '13800000009', 'user5@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user6', '13800000010', 'user6@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
-- 新增用户
('doctor3', '13800000011', 'doctor3@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('doctor4', '13800000012', 'doctor4@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user7', '13800000013', 'user7@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user8', '13800000014', 'user8@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user9', '13800000015', 'user9@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW()),
('user10', '13800000016', 'user10@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', NULL, 1, NOW(), NOW());

-- 1.4 插入用户角色关联数据
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 1),   -- admin用户拥有admin角色
(2, 2),   -- doctor1拥有doctor角色
(3, 2),   -- doctor2拥有doctor角色
(4, 3),   -- user1拥有user角色
(5, 3),   -- user2拥有user角色
(6, 3),   -- user3拥有user角色
(7, 4),   -- reviewer1拥有reviewer角色
(8, 3),   -- user4拥有user角色
(9, 3),   -- user5拥有user角色
(10, 3),  -- user6拥有user角色
-- 新增用户的角色分配
(11, 2),  -- doctor3拥有doctor角色
(12, 2),  -- doctor4拥有doctor角色
(13, 3),  -- user7拥有user角色
(14, 3),  -- user8拥有user角色
(15, 3),  -- user9拥有user角色
(16, 3);  -- user10拥有user角色

-- 1.5 插入角色权限关联数据
INSERT INTO role_permissions (role_id, permission_id) VALUES
-- admin角色拥有所有权限
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14),
-- doctor角色权限
(2, 2), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
-- user角色权限
(3, 2), (3, 5), (3, 6), (3, 9),
-- reviewer角色权限
(4, 2), (4, 6), (4, 7), (4, 9), (4, 12);

-- ============================================
-- 2. 医生管理模块数据
-- ============================================

-- 2.1 插入医生数据
INSERT INTO doctors (name, gender, age, department, title, specialties, introduction, phone, email, status) VALUES
('张医生', 1, 45, '内科', '主任医师', '心血管疾病、高血压、糖尿病', '从事临床工作20余年，擅长心血管疾病的诊断和治疗。', '13800000002', 'doctor1@example.com', 1),
('李医生', 0, 38, '儿科', '副主任医师', '儿童常见病、生长发育、营养指导', '专注于儿科临床工作15年，对儿童常见病有丰富的诊疗经验。', '13800000003', 'doctor2@example.com', 1),
('王医生', 1, 42, '外科', '主任医师', '普外科、微创手术、肿瘤外科', '外科手术经验丰富，擅长微创手术技术。', '13900000011', 'doctor3@example.com', 1),
('赵医生', 0, 35, '妇科', '主治医师', '妇科常见病、妇科肿瘤、不孕不育', '专注于妇科疾病的诊断和治疗。', '13900000012', 'doctor4@example.com', 1),
('刘医生', 1, 50, '骨科', '主任医师', '骨科创伤、关节疾病、脊柱外科', '从事骨科临床工作25年，经验丰富。', '13900000013', 'doctor5@example.com', 1),
-- 新增医生
('陈医生', 0, 40, '神经内科', '副主任医师', '脑血管疾病、癫痫、帕金森病', '从事神经内科临床工作15年。', '13900000014', 'doctor6@example.com', 1),
('孙医生', 1, 48, '心内科', '主任医师', '冠心病、心律失常、心力衰竭', '心血管疾病介入治疗专家。', '13900000015', 'doctor7@example.com', 1),
('周医生', 0, 36, '消化内科', '主治医师', '胃炎、胃溃疡、结肠炎', '擅长消化系统疾病诊疗。', '13900000016', 'doctor8@example.com', 1),
('吴医生', 1, 52, '呼吸内科', '主任医师', '肺炎、支气管哮喘、慢性阻塞性肺病', '呼吸系统疾病专家。', '13900000017', 'doctor9@example.com', 1),
('郑医生', 0, 33, '内分泌科', '主治医师', '糖尿病、甲状腺疾病、骨质疏松', '专注于内分泌代谢疾病。', '13900000018', 'doctor10@example.com', 1);

-- 2.2 插入排班数据
INSERT INTO schedules (doctor_id, date, start_time, end_time, status) VALUES
-- 张医生的排班
(1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '09:00:00', '12:00:00', 1),
(1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '14:00:00', '17:00:00', 1),
(1, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '09:00:00', '12:00:00', 1),
(1, DATE_ADD(CURDATE(), INTERVAL 5 DAY), '09:00:00', '12:00:00', 1),
(1, DATE_ADD(CURDATE(), INTERVAL 7 DAY), '14:00:00', '17:00:00', 1),
-- 李医生的排班
(2, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00:00', '12:00:00', 1),
(2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '14:00:00', '18:00:00', 1),
(2, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '08:00:00', '12:00:00', 1),
-- 王医生的排班
(3, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '09:00:00', '12:00:00', 1),
(3, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '14:00:00', '17:00:00', 1),
(3, DATE_ADD(CURDATE(), INTERVAL 6 DAY), '09:00:00', '12:00:00', 1),
-- 赵医生的排班
(4, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '10:00:00', '13:00:00', 1),
(4, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '14:00:00', '17:00:00', 1),
-- 刘医生的排班
(5, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '08:00:00', '12:00:00', 1),
(5, DATE_ADD(CURDATE(), INTERVAL 5 DAY), '14:00:00', '18:00:00', 1),
-- 新增医生的排班
(6, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '09:00:00', '12:00:00', 1),
(6, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '14:00:00', '17:00:00', 1),
(7, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '09:00:00', '12:00:00', 1),
(7, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '14:00:00', '17:00:00', 1),
(8, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00:00', '12:00:00', 1),
(9, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '09:00:00', '12:00:00', 1),
(10, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '14:00:00', '17:00:00', 1);

-- ============================================
-- 3. 问诊服务模块数据
-- ============================================

-- 3.1 插入问诊记录数据
INSERT INTO consultation_records (user_id, doctor_id, symptoms, conversation_history, ai_suggestion, status) VALUES
-- 问诊1：已完成
(4, 1, '头痛、发热、咳嗽',
 '{"messages": [{"role": "user", "content": "我最近头痛、发热，还咳嗽"}, {"role": "ai", "content": "请问您发热多少度？持续多久了？"}, {"role": "user", "content": "发热38.5度，已经持续2天了"}, {"role": "ai", "content": "根据您的症状，建议多休息，多喝水，可以服用退烧药。如症状持续或加重，建议就医。"}]}',
 '根据症状描述，建议测量体温，多休息，多喝水。如症状持续，建议就医。', 1),
-- 问诊2：已完成
(5, 2, '儿童发烧、食欲不振',
 '{"messages": [{"role": "user", "content": "孩子3岁，发烧38度，不想吃饭"}, {"role": "ai", "content": "孩子发烧多久了？有没有其他症状？"}, {"role": "user", "content": "昨天开始的，没有其他明显症状"}, {"role": "ai", "content": "建议物理降温，观察孩子精神状态。如持续高烧或精神状态差，及时就医。"}]}',
 '建议物理降温，观察孩子精神状态。如持续高烧或精神状态差，及时就医。', 1),
-- 问诊3：进行中
(6, NULL, '胸闷、气短',
 '{"messages": [{"role": "user", "content": "最近感觉胸闷、气短"}, {"role": "ai", "content": "这种情况持续多久了？有没有其他不适？"}, {"role": "user", "content": "持续一周了，没有其他症状"}, {"role": "ai", "content": "建议进行心电图和胸部CT检查，排除心脏和肺部疾病。"}]}',
 '建议进行心电图和胸部CT检查，排除心脏和肺部疾病。', 0),
-- 问诊4：已完成
(8, 1, '高血压、头晕',
 '{"messages": [{"role": "user", "content": "血压偏高，经常头晕"}, {"role": "ai", "content": "血压具体数值是多少？平时有服药吗？"}]}',
 '建议监测血压，规律服药，低盐饮食，适量运动。', 1),
-- 问诊5：待审核
(9, NULL, '胃痛、消化不良',
 '{"messages": [{"role": "user", "content": "胃痛，吃东西不消化"}, {"role": "ai", "content": "疼痛是持续性的还是间歇性的？"}]}',
 '建议清淡饮食，避免辛辣刺激食物，如症状持续建议做胃镜检查。', 3),
-- 新增问诊记录
-- 问诊6：已完成
(13, 3, '阑尾炎术后护理',
 '{"messages": [{"role": "user", "content": "刚做完阑尾炎手术需要注意什么？"}, {"role": "ai", "content": "术后多长时间了？目前有什么不适吗？"}, {"role": "user", "content": "手术一周了，伤口愈合还可以"}, {"role": "ai", "content": "建议注意休息，清淡饮食，定期换药，如有发热或伤口异常及时就医。"}]}',
 '建议注意休息，清淡饮食，定期换药，如有发热或伤口异常及时就医。', 1),
-- 问诊7：已取消
(14, NULL, '痛经',
 '{"messages": [{"role": "user", "content": "每个月来月经都痛经很厉害"}]}',
 '建议热敷腹部，如疼痛剧烈可服用止痛药，建议就医检查。', 2),
-- 问诊8：已完成
(15, 6, '头痛、眩晕',
 '{"messages": [{"role": "user", "content": "最近经常头痛，还伴有眩晕"}, {"role": "ai", "content": "这种情况持续多久了？有没有恶心呕吐？"}, {"role": "user", "content": "持续一周了，有时会恶心"}, {"role": "ai", "content": "建议进行头颅CT或MRI检查，排除颅内病变。"}]}',
 '建议进行头颅CT或MRI检查，排除颅内病变。', 1),
-- 问诊9：已完成
(16, 7, '胸痛、心悸',
 '{"messages": [{"role": "user", "content": "最近经常胸痛，心跳也很快"}, {"role": "ai", "content": "胸痛多长时间了？与活动有没有关系？"}, {"role": "user", "content": "活动后更明显，休息后能缓解"}, {"role": "ai", "content": "建议尽快就医，进行心电图和心脏超声检查。"}]}',
 '建议尽快就医，进行心电图和心脏超声检查。', 1),
-- 问诊10：进行中
(4, NULL, '失眠',
 '{"messages": [{"role": "user", "content": "最近失眠严重，睡不着觉"}]}',
 '建议保持规律作息，睡前避免使用电子设备，必要时可就医。', 0),
-- 问诊11：已完成
(5, 8, '胃痛、反酸',
 '{"messages": [{"role": "user", "content": "胃痛，反酸水"}, {"role": "ai", "content": "这种情况有多久了？饭前还是饭后加重？"}, {"role": "user", "content": "半年了，饭后更明显"}, {"role": "ai", "content": "建议做胃镜检查，规律饮食，避免辛辣刺激食物。"}]}',
 '建议做胃镜检查，规律饮食，避免辛辣刺激食物。', 1),
-- 问诊12：已完成
(6, 9, '咳嗽、咳痰',
 '{"messages": [{"role": "user", "content": "感冒后一直咳嗽，有痰"}, {"role": "ai", "content": "咳嗽多长时间了？痰是什么颜色的？"}, {"role": "user", "content": "两周了，痰是白色的"}, {"role": "ai", "content": "建议多喝水，必要时服用止咳化痰药物，如症状加重就就医。"}]}',
 '建议多喝水，必要时服用止咳化痰药物，如症状加重就就医。', 1);

-- 3.2 插入问诊消息数据
INSERT INTO consultation_messages (consultation_id, sender_type, content) VALUES
-- 问诊1的消息
(1, 'user', '我最近头痛、发热，还咳嗽'),
(1, 'ai', '请问您发热多少度？持续多久了？'),
(1, 'user', '发热38.5度，已经持续2天了'),
(1, 'ai', '根据您的症状，建议多休息，多喝水，可以服用退烧药。如症状持续或加重，建议就医。'),
-- 问诊2的消息
(2, 'user', '孩子3岁，发烧38度，不想吃饭'),
(2, 'ai', '孩子发烧多久了？有没有其他症状？'),
(2, 'user', '昨天开始的，没有其他明显症状'),
(2, 'ai', '建议物理降温，观察孩子精神状态。如持续高烧或精神状态差，及时就医。'),
-- 问诊3的消息
(3, 'user', '最近感觉胸闷、气短'),
(3, 'ai', '这种情况持续多久了？有没有其他不适？'),
(3, 'user', '持续一周了，没有其他症状'),
(3, 'ai', '建议进行心电图和胸部CT检查，排除心脏和肺部疾病。'),
-- 问诊4的消息
(4, 'user', '血压偏高，经常头晕'),
(4, 'ai', '血压具体数值是多少？平时有服药吗？'),
(4, 'user', '一般在150/95左右，服用降压药'),
(4, 'ai', '建议监测血压变化，坚持服药，低盐饮食，适量运动，定期复查。'),
-- 问诊5的消息
(5, 'user', '胃痛，吃东西不消化'),
(5, 'ai', '疼痛是持续性的还是间歇性的？'),
(5, 'user', '饭后半小时就开始疼'),
(5, 'ai', '建议清淡饮食，避免辛辣刺激食物，如症状持续建议做胃镜检查。'),
-- 新增问诊消息
-- 问诊6的消息
(6, 'user', '刚做完阑尾炎手术需要注意什么？'),
(6, 'ai', '术后多长时间了？目前有什么不适吗？'),
(6, 'user', '手术一周了，伤口愈合还可以'),
(6, 'ai', '建议注意休息，清淡饮食，定期换药，如有发热或伤口异常及时就医。'),
-- 问诊7的消息
(7, 'user', '每个月来月经都痛经很厉害'),
(7, 'ai', '痛经会影响日常生活吗？有没有尝试过什么方法缓解？'),
(7, 'user', '是的，很影响，能吃的止痛药都吃了'),
(7, 'ai', '建议热敷腹部，如疼痛剧烈可服用止痛药，建议就医检查。'),
-- 问诊8的消息
(8, 'user', '最近经常头痛，还伴有眩晕'),
(8, 'ai', '这种情况持续多久了？有没有恶心呕吐？'),
(8, 'user', '持续一周了，有时会恶心'),
(8, 'ai', '建议进行头颅CT或MRI检查，排除颅内病变。'),
-- 问诊9的消息
(9, 'user', '最近经常胸痛，心跳也很快'),
(9, 'ai', '胸痛多长时间了？与活动有没有关系？'),
(9, 'user', '活动后更明显，休息后能缓解'),
(9, 'ai', '建议尽快就医，进行心电图和心脏超声检查。'),
-- 问诊10的消息
(10, 'user', '最近失眠严重，睡不着觉'),
(10, 'ai', '失眠多长时间了？睡前有什么习惯吗？'),
(10, 'user', '一个月了，睡前看手机'),
(10, 'ai', '建议保持规律作息，睡前避免使用电子设备，必要时可就医。'),
-- 问诊11的消息
(11, 'user', '胃痛，反酸水'),
(11, 'ai', '这种情况有多久了？饭前还是饭后加重？'),
(11, 'user', '半年了，饭后更明显'),
(11, 'ai', '建议做胃镜检查，规律饮食，避免辛辣刺激食物。'),
-- 问诊12的消息
(12, 'user', '感冒后一直咳嗽，有痰'),
(12, 'ai', '咳嗽多长时间了？痰是什么颜色的？'),
(12, 'user', '两周了，痰是白色的'),
(12, 'ai', '建议多喝水，必要时服用止咳化痰药物，如症状加重就就医。');

-- 3.3 插入AI报告数据
INSERT INTO ai_reports (consultation_id, report_content, report_type) VALUES
(1, '{"diagnosis": "上呼吸道感染", "symptoms": ["头痛", "发热", "咳嗽"], "suggestion": "多休息，多喝水，可服用退烧药和止咳药", "severity": "轻度"}', 'text'),
(2, '{"diagnosis": "儿童发热", "symptoms": ["发烧", "食欲不振"], "suggestion": "物理降温，观察精神状态，必要时就医", "severity": "轻度"}', 'text'),
(4, '{"diagnosis": "高血压", "symptoms": ["血压偏高", "头晕"], "suggestion": "监测血压，规律服药，低盐饮食，适量运动", "severity": "中度"}', 'text'),
-- 新增AI报告
(6, '{"diagnosis": "阑尾炎术后", "symptoms": ["术后恢复"], "suggestion": "注意休息，清淡饮食，定期换药", "severity": "轻度"}', 'text'),
(8, '{"diagnosis": "头痛待查", "symptoms": ["头痛", "眩晕", "恶心"], "suggestion": "头颅CT或MRI检查", "severity": "中度"}', 'text'),
(9, '{"diagnosis": "冠心病待查", "symptoms": ["胸痛", "心悸"], "suggestion": "心电图和心脏超声检查", "severity": "中度"}', 'text'),
(11, '{"diagnosis": "慢性胃炎", "symptoms": ["胃痛", "反酸"], "suggestion": "胃镜检查，规律饮食", "severity": "轻度"}', 'text'),
(12, '{"diagnosis": "支气管炎", "symptoms": ["咳嗽", "咳痰"], "suggestion": "多喝水，止咳化痰药物", "severity": "轻度"}', 'text');

-- ============================================
-- 4. 健康管理模块数据
-- ============================================

-- 4.1 插入健康档案数据
INSERT INTO health_records (user_id, blood_type, height, weight, medical_history, family_history, allergy_history) VALUES
(4, 'A', 175.00, 70.00, '无', '父亲有高血压', '无'),
(5, 'B', 168.00, 65.00, '胃炎', '无', '青霉素过敏'),
(6, 'O', 180.00, 75.00, '无', '母亲有糖尿病', '无'),
(8, 'AB', 172.00, 80.00, '高血压', '父亲有高血压、心脏病', '无'),
(9, 'A', 165.00, 60.00, '无', '无', '海鲜过敏'),
(10, 'B', 178.00, 72.00, '无', '无', '无'),
-- 新增健康档案
(13, 'A', 170.00, 68.00, '阑尾炎手术史', '无', '无'),
(14, 'O', 162.00, 55.00, '痛经', '母亲有痛经史', '无'),
(15, 'AB', 175.00, 78.00, '无', '父亲有高血压', '无'),
(16, 'B', 168.00, 62.00, '无', '无', '无');

-- 4.2 插入体征数据
INSERT INTO vital_signs (user_id, sign_type, value, unit, measured_at, notes) VALUES
-- 用户4的体征数据
(4, '血压', 120.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 3 DAY), '正常'),
(4, '血压', 125.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 2 DAY), '略高'),
(4, '血压', 122.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(4, '血压', 118.00, 'mmHg', NOW(), '正常'),
(4, '心率', 72.00, '次/分', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(4, '心率', 70.00, '次/分', NOW(), '正常'),
(4, '体温', 36.50, '℃', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(4, '体温', 36.80, '℃', NOW(), '正常'),
-- 用户5的体征数据
(5, '血压', 110.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 3 DAY), '正常'),
(5, '血压', 108.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 2 DAY), '正常'),
(5, '血压', 112.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(5, '心率', 68.00, '次/分', DATE_SUB(NOW(), INTERVAL 2 DAY), '正常'),
(5, '心率', 70.00, '次/分', NOW(), '正常'),
(5, '体温', 36.60, '℃', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(5, '体温', 36.80, '℃', NOW(), '正常'),
-- 用户6的体征数据
(6, '血压', 130.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 2 DAY), '偏高'),
(6, '血压', 128.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 1 DAY), '略高'),
(6, '血压', 125.00, 'mmHg', NOW(), '正常'),
(6, '心率', 75.00, '次/分', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(6, '心率', 72.00, '次/分', NOW(), '正常'),
-- 用户8的体征数据
(8, '血压', 150.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 3 DAY), '偏高'),
(8, '血压', 145.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 2 DAY), '偏高'),
(8, '血压', 148.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 1 DAY), '偏高'),
(8, '血压', 142.00, 'mmHg', NOW(), '偏高，需注意'),
(8, '血糖', 6.80, 'mmol/L', DATE_SUB(NOW(), INTERVAL 2 DAY), '略高'),
(8, '血糖', 6.50, 'mmol/L', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(8, '血糖', 6.20, 'mmol/L', NOW(), '正常'),
(8, '心率', 80.00, '次/分', NOW(), '偏快'),
-- 用户9的体征数据
(9, '血压', 115.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 2 DAY), '正常'),
(9, '血压', 118.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(9, '血压', 112.00, 'mmHg', NOW(), '正常'),
(9, '心率', 70.00, '次/分', DATE_SUB(NOW(), INTERVAL 1 DAY), '正常'),
(9, '心率', 68.00, '次/分', NOW(), '正常'),
-- 用户10的体征数据
(10, '血压', 120.00, 'mmHg', NOW(), '正常'),
(10, '心率', 75.00, '次/分', NOW(), '正常'),
(10, '体温', 36.50, '℃', NOW(), '正常'),
-- 新增用户的体征数据
-- 用户13的体征数据
(13, '血压', 115.00, 'mmHg', NOW(), '正常'),
(13, '心率', 72.00, '次/分', NOW(), '正常'),
(13, '体温', 36.60, '℃', NOW(), '正常'),
-- 用户14的体征数据
(14, '血压', 110.00, 'mmHg', NOW(), '正常'),
(14, '心率', 76.00, '次/分', NOW(), '正常'),
-- 用户15的体征数据
(15, '血压', 135.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 2 DAY), '偏高'),
(15, '血压', 138.00, 'mmHg', DATE_SUB(NOW(), INTERVAL 1 DAY), '偏高'),
(15, '血压', 130.00, 'mmHg', NOW(), '略高'),
(15, '心率', 78.00, '次/分', NOW(), '正常'),
-- 用户16的体征数据
(16, '血压', 118.00, 'mmHg', NOW(), '正常'),
(16, '心率', 70.00, '次/分', NOW(), '正常');

-- 4.3 插入检查记录数据
INSERT INTO examination_records (user_id, examination_type, examination_data, examination_date, hospital_name, doctor_name) VALUES
(4, '血常规', '{"白细胞": 6.5, "红细胞": 4.8, "血小板": 200, "血红蛋白": 140}', DATE_SUB(CURDATE(), INTERVAL 30 DAY), '市人民医院', '张医生'),
(4, '尿常规', '{"尿蛋白": "阴性", "尿糖": "阴性", "白细胞": "0-2", "PH值": 6.0}', DATE_SUB(CURDATE(), INTERVAL 60 DAY), '市人民医院', '张医生'),
(5, '尿常规', '{"尿蛋白": "阴性", "尿糖": "阴性", "白细胞": "0-2"}', DATE_SUB(CURDATE(), INTERVAL 15 DAY), '市人民医院', '李医生'),
(5, '胃镜检查', '{"诊断": "慢性浅表性胃炎", "建议": "注意饮食"}', DATE_SUB(CURDATE(), INTERVAL 90 DAY), '市人民医院', '周医生'),
(6, '心电图', '{"心率": 75, "心律": "窦性", "结论": "正常"}', DATE_SUB(CURDATE(), INTERVAL 7 DAY), '市人民医院', '王医生'),
(6, '血常规', '{"白细胞": 7.2, "红细胞": 5.0, "血小板": 220, "血红蛋白": 150}', DATE_SUB(CURDATE(), INTERVAL 45 DAY), '市人民医院', '王医生'),
(8, '血压监测', '{"收缩压": 145, "舒张压": 95, "平均压": 112}', DATE_SUB(CURDATE(), INTERVAL 5 DAY), '市人民医院', '张医生'),
(8, '血糖监测', '{"空腹血糖": 6.5, "餐后血糖": 8.2, "糖化血红蛋白": 6.8}', DATE_SUB(CURDATE(), INTERVAL 20 DAY), '市人民医院', '郑医生'),
(8, '血脂检查', '{"总胆固醇": 5.8, "甘油三酯": 2.1, "高密度脂蛋白": 1.2, "低密度脂蛋白": 3.5}', DATE_SUB(CURDATE(), INTERVAL 45 DAY), '市人民医院', '孙医生'),
(9, '胃镜检查', '{"诊断": "慢性浅表性胃炎", "建议": "注意饮食"}', DATE_SUB(CURDATE(), INTERVAL 20 DAY), '市人民医院', '赵医生'),
(9, '血常规', '{"白细胞": 6.0, "红细胞": 4.5, "血小板": 190, "血红蛋白": 130}', DATE_SUB(CURDATE(), INTERVAL 90 DAY), '市人民医院', '周医生'),
(10, '血常规', '{"白细胞": 6.8, "红细胞": 4.9, "血小板": 210, "血红蛋白": 145}', DATE_SUB(CURDATE(), INTERVAL 30 DAY), '市人民医院', '张医生'),
-- 新增检查记录
(13, '腹部CT', '{"诊断": "阑尾炎术后改变", "结论": "恢复良好"}', DATE_SUB(CURDATE(), INTERVAL 10 DAY), '市人民医院', '王医生'),
(14, 'B超检查', '{"子宫": "未见明显异常", "卵巢": "未见明显异常"}', DATE_SUB(CURDATE(), INTERVAL 60 DAY), '市人民医院', '赵医生'),
(15, '心电图', '{"心率": 78, "心律": "窦性", "结论": "大致正常"}', DATE_SUB(CURDATE(), INTERVAL 15 DAY), '市人民医院', '孙医生'),
(15, '心脏超声', '{"左室射血分数": "60%", "结论": "心功能正常"}', DATE_SUB(CURDATE(), INTERVAL 30 DAY), '市人民医院', '孙医生'),
(16, '血常规', '{"白细胞": 6.2, "红细胞": 4.7, "血小板": 205, "血红蛋白": 142}', DATE_SUB(CURDATE(), INTERVAL 45 DAY), '市人民医院', '张医生');

-- 4.4 插入疫苗接种记录数据
INSERT INTO vaccination_records (user_id, vaccine_name, vaccination_date, vaccination_agency, batch_number, next_vaccination_date, notes) VALUES
(4, '新冠疫苗（第一针）', DATE_SUB(CURDATE(), INTERVAL 365 DAY), '社区卫生服务中心', 'CN2023001', DATE_SUB(CURDATE(), INTERVAL 300 DAY), '已完成'),
(4, '新冠疫苗（第二针）', DATE_SUB(CURDATE(), INTERVAL 300 DAY), '社区卫生服务中心', 'CN2023002', DATE_SUB(CURDATE(), INTERVAL 235 DAY), '已完成'),
(4, '新冠疫苗（第三针）', DATE_SUB(CURDATE(), INTERVAL 180 DAY), '社区卫生服务中心', 'CN2024001', NULL, '已完成'),
(4, '流感疫苗', DATE_SUB(CURDATE(), INTERVAL 120 DAY), '社区卫生服务中心', 'FL2024001', DATE_ADD(CURDATE(), INTERVAL 245 DAY), '正常'),
(5, '流感疫苗', DATE_SUB(CURDATE(), INTERVAL 60 DAY), '社区卫生服务中心', 'FL2024001', DATE_ADD(CURDATE(), INTERVAL 305 DAY), '正常'),
(5, '乙肝疫苗', DATE_SUB(CURDATE(), INTERVAL 180 DAY), '社区卫生服务中心', 'HB2023001', NULL, '已完成'),
(6, '新冠疫苗（第一针）', DATE_SUB(CURDATE(), INTERVAL 400 DAY), '社区卫生服务中心', 'CN2022001', DATE_SUB(CURDATE(), INTERVAL 335 DAY), '已完成'),
(6, '新冠疫苗（第二针）', DATE_SUB(CURDATE(), INTERVAL 335 DAY), '社区卫生服务中心', 'CN2022002', DATE_SUB(CURDATE(), INTERVAL 270 DAY), '已完成'),
(6, '新冠疫苗（第三针）', DATE_SUB(CURDATE(), INTERVAL 200 DAY), '社区卫生服务中心', 'CN2024002', NULL, '已完成'),
(8, '乙肝疫苗', DATE_SUB(CURDATE(), INTERVAL 90 DAY), '社区卫生服务中心', 'HB2024001', DATE_ADD(CURDATE(), INTERVAL 275 DAY), '正常'),
(8, '流感疫苗', DATE_SUB(CURDATE(), INTERVAL 150 DAY), '社区卫生服务中心', 'FL2023002', DATE_ADD(CURDATE(), INTERVAL 215 DAY), '已完成'),
(9, '流感疫苗', DATE_SUB(CURDATE(), INTERVAL 45 DAY), '社区卫生服务中心', 'FL2024002', DATE_ADD(CURDATE(), INTERVAL 320 DAY), '正常'),
(9, '新冠疫苗（第三针）', DATE_SUB(CURDATE(), INTERVAL 220 DAY), '社区卫生服务中心', 'CN2024003', NULL, '已完成'),
(10, '新冠疫苗（第三针）', DATE_SUB(CURDATE(), INTERVAL 200 DAY), '社区卫生服务中心', 'CN2024004', NULL, '已完成'),
-- 新增疫苗接种记录
(13, '破伤风疫苗', DATE_SUB(CURDATE(), INTERVAL 15 DAY), '市人民医院', 'TT2024001', NULL, '术后接种'),
(14, 'HPV疫苗（第一针）', DATE_SUB(CURDATE(), INTERVAL 90 DAY), '社区卫生服务中心', 'HPV2024001', DATE_SUB(CURDATE(), INTERVAL 30 DAY), '已完成'),
(14, 'HPV疫苗（第二针）', DATE_SUB(CURDATE(), INTERVAL 30 DAY), '社区卫生服务中心', 'HPV2024002', DATE_ADD(CURDATE(), INTERVAL 60 DAY), '正常'),
(15, '流感疫苗', DATE_SUB(CURDATE(), INTERVAL 100 DAY), '社区卫生服务中心', 'FL2024003', DATE_ADD(CURDATE(), INTERVAL 265 DAY), '正常'),
(16, '新冠疫苗（第三针）', DATE_SUB(CURDATE(), INTERVAL 180 DAY), '社区卫生服务中心', 'CN2024005', NULL, '已完成');

-- 4.5 插入用药记录数据
INSERT INTO medication_records (user_id, medication_name, dosage, frequency, start_date, end_date, reminder_enabled, reminder_times, notes) VALUES
(4, '布洛芬', '200mg', '每日3次，饭后服用', DATE_SUB(CURDATE(), INTERVAL 3 DAY), DATE_ADD(CURDATE(), INTERVAL 4 DAY), 1, '["08:00", "14:00", "20:00"]', '退烧止痛'),
(4, '感冒灵颗粒', '10g', '每日3次，冲服', DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(CURDATE(), INTERVAL 2 DAY), 1, '["08:00", "12:00", "18:00"]', '治疗感冒'),
(5, '奥美拉唑', '20mg', '每日1次，饭前服用', DATE_SUB(CURDATE(), INTERVAL 10 DAY), DATE_ADD(CURDATE(), INTERVAL 20 DAY), 1, '["07:00"]', '治疗胃炎'),
(5, '铝碳酸镁片', '1g', '每日3次，饭后服用', DATE_SUB(CURDATE(), INTERVAL 10 DAY), DATE_ADD(CURDATE(), INTERVAL 20 DAY), 1, '["08:00", "14:00", "20:00"]', '中和胃酸'),
(6, '阿司匹林', '100mg', '每日1次，饭后服用', DATE_SUB(CURDATE(), INTERVAL 60 DAY), NULL, 1, '["08:00"]', '预防心血管疾病'),
(8, '硝苯地平', '10mg', '每日2次，早晚各一次', DATE_SUB(CURDATE(), INTERVAL 30 DAY), NULL, 1, '["08:00", "20:00"]', '降血压'),
(8, '二甲双胍', '500mg', '每日2次，饭后服用', DATE_SUB(CURDATE(), INTERVAL 45 DAY), NULL, 1, '["08:00", "18:00"]', '控制血糖'),
(8, '阿托伐他汀', '20mg', '每日1次，睡前服用', DATE_SUB(CURDATE(), INTERVAL 60 DAY), NULL, 1, '["21:00"]', '降血脂'),
(9, '多潘立酮', '10mg', '每日3次，饭前服用', DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_ADD(CURDATE(), INTERVAL 10 DAY), 1, '["07:00", "12:00", "18:00"]', '助消化'),
(9, '奥美拉唑', '20mg', '每日1次，饭前服用', DATE_SUB(CURDATE(), INTERVAL 15 DAY), DATE_ADD(CURDATE(), INTERVAL 45 DAY), 1, '["07:00"]', '治疗胃炎'),
(10, '维生素C', '100mg', '每日1次，饭后服用', DATE_SUB(CURDATE(), INTERVAL 30 DAY), NULL, 1, '["08:00"]', '补充维生素'),
-- 新增用药记录
(13, '头孢克肟', '200mg', '每日2次，饭后服用', DATE_SUB(CURDATE(), INTERVAL 7 DAY), DATE_ADD(CURDATE(), INTERVAL 7 DAY), 1, '["08:00", "20:00"]', '预防感染'),
(14, '布洛芬', '200mg', '每日3次，饭后服用', DATE_SUB(CURDATE(), INTERVAL 2 DAY), DATE_ADD(CURDATE(), INTERVAL 3 DAY), 1, '["08:00", "14:00", "20:00"]', '缓解痛经'),
(15, '硝酸甘油', '0.5mg', '胸痛时舌下含服', DATE_SUB(CURDATE(), INTERVAL 10 DAY), NULL, 1, '["08:00"]', '缓解胸痛'),
(16, '蒙脱石散', '3g', '每日3次，冲服', DATE_SUB(CURDATE(), INTERVAL 2 DAY), DATE_ADD(CURDATE(), INTERVAL 3 DAY), 1, '["08:00", "14:00", "20:00"]', '治疗腹泻');

-- ============================================
-- 5. 内容管理模块数据
-- ============================================

-- 5.1 插入分类数据
INSERT INTO categories (category_name, parent_id, sort_order, description, status) VALUES
('健康资讯', NULL, 1, '健康相关的资讯文章', 1),
('疾病科普', NULL, 2, '各类疾病的科普知识', 1),
('养生保健', NULL, 3, '养生保健相关文章', 1),
('心血管疾病', 2, 1, '心血管疾病相关', 1),
('消化系统疾病', 2, 2, '消化系统疾病相关', 1),
('呼吸系统疾病', 2, 3, '呼吸系统疾病相关', 1),
('儿童健康', 1, 1, '儿童健康相关资讯', 1),
('女性健康', 1, 2, '女性健康相关资讯', 1),
-- 新增分类
('神经系统疾病', 2, 4, '神经系统疾病相关', 1),
('内分泌疾病', 2, 5, '内分泌疾病相关', 1),
('骨科疾病', 2, 6, '骨科疾病相关', 1),
('四季养生', 3, 1, '四季养生相关文章', 1),
('饮食养生', 3, 2, '饮食养生相关文章', 1),
('运动养生', 3, 3, '运动养生相关文章', 1),
('心理健康', 1, 3, '心理健康相关资讯', 1);

-- 5.2 插入文章数据
INSERT INTO articles (doctor_id, category_id, title, content, cover_image, tags, status, view_count, like_count, published_at) VALUES
(1, 4, '高血压的预防与治疗',
 '高血压是一种常见的慢性疾病，长期高血压会对心、脑、肾等器官造成损害。预防高血压的关键在于：1. 合理饮食，低盐低脂；2. 适量运动；3. 控制体重；4. 戒烟限酒；5. 保持心情舒畅。治疗方面，应在医生指导下规律服药，定期监测血压。',
 NULL, '高血压,心血管,预防,治疗', 2, 1250, 85, DATE_SUB(NOW(), INTERVAL 10 DAY)),
(2, 7, '儿童发热的家庭护理',
 '儿童发热是常见症状，家长应掌握正确的护理方法：1. 测量体温，38.5度以下可物理降温；2. 多喝水，保持室内通风；3. 观察孩子精神状态；4. 如持续高烧或出现其他症状，及时就医。',
 NULL, '儿童,发热,护理', 2, 980, 62, DATE_SUB(NOW(), INTERVAL 8 DAY)),
(1, 4, '冠心病的早期症状识别',
 '冠心病早期可能出现的症状包括：胸痛、胸闷、气短、心悸等。如果出现这些症状，应及时就医检查。预防冠心病需要控制危险因素，如高血压、高血脂、糖尿病等。',
 NULL, '冠心病,心血管,症状', 2, 756, 45, DATE_SUB(NOW(), INTERVAL 5 DAY)),
(3, 5, '胃炎的饮食调理',
 '胃炎患者应注意饮食调理：1. 规律饮食，少食多餐；2. 避免辛辣、生冷、油腻食物；3. 多吃易消化的食物；4. 戒烟限酒；5. 保持心情愉快。',
 NULL, '胃炎,消化系统,饮食', 2, 634, 38, DATE_SUB(NOW(), INTERVAL 3 DAY)),
(2, 7, '儿童营养与生长发育',
 '儿童期是生长发育的关键时期，营养摄入要均衡。应保证蛋白质、维生素、矿物质等营养素的充足摄入，同时注意培养良好的饮食习惯。',
 NULL, '儿童,营养,生长发育', 2, 542, 29, DATE_SUB(NOW(), INTERVAL 1 DAY)),
(1, 1, '春季养生小贴士',
 '春季是养生的好时节，应注意：1. 早睡早起；2. 适量运动；3. 饮食清淡；4. 保持心情舒畅；5. 注意保暖，预防感冒。',
 NULL, '春季,养生,健康', 2, 432, 25, DATE_SUB(NOW(), INTERVAL 2 DAY)),
(4, 8, '女性更年期的健康管理',
 '更年期是女性生命中的一个重要阶段，应注意：1. 保持规律作息；2. 适量运动；3. 均衡饮食；4. 定期体检；5. 保持心情愉快。',
 NULL, '女性,更年期,健康', 2, 356, 22, DATE_SUB(NOW(), INTERVAL 6 DAY)),
-- 新增文章
(6, 9, '头痛的常见原因及预防',
 '头痛是常见的症状，常见原因包括：1. 紧张性头痛；2. 偏头痛；3. 颅内病变；4. 高血压等。预防头痛需要注意休息、规律作息、避免精神紧张。',
 NULL, '头痛,神经系统,预防', 2, 425, 31, DATE_SUB(NOW(), INTERVAL 4 DAY)),
(7, 4, '心律失常的识别与处理',
 '心律失常是指心脏跳动节律异常，常见类型包括早搏、房颤、室上性心动过速等。出现心悸、胸闷等症状时应及时就医，进行心电图检查。',
 NULL, '心律失常,心血管,心脏', 2, 389, 28, DATE_SUB(NOW(), INTERVAL 7 DAY)),
(8, 5, '胃溃疡的饮食禁忌',
 '胃溃疡患者饮食应注意：1. 定时定量，少食多餐；2. 避免刺激性食物；3. 细嚼慢咽；4. 戒烟戒酒；5. 保持心情愉快。',
 NULL, '胃溃疡,消化系统,饮食', 2, 298, 19, DATE_SUB(NOW(), INTERVAL 9 DAY)),
(9, 6, '支气管哮喘的日常管理',
 '支气管哮喘是一种慢性气道炎症性疾病，日常管理包括：1. 避免接触过敏原；2. 规律使用控制药物；3. 定期复查肺功能；4. 随身携带急救药物。',
 NULL, '哮喘,呼吸系统,慢性病', 2, 412, 33, DATE_SUB(NOW(), INTERVAL 5 DAY)),
(10, 10, '糖尿病的饮食控制',
 '糖尿病患者饮食控制是关键：1. 控制总热量；2. 均衡营养；3. 低糖低脂；4. 多吃蔬菜；5. 定时定量。',
 NULL, '糖尿病,内分泌,饮食', 2, 567, 41, DATE_SUB(NOW(), INTERVAL 3 DAY)),
(1, 12, '夏季养生注意事项',
 '夏季养生应注意：1. 防暑降温；2. 合理饮食；3. 适当运动；4. 充足睡眠；5. 调节情绪。',
 NULL, '夏季,养生,季节', 2, 378, 24, DATE_SUB(NOW(), INTERVAL 11 DAY)),
(5, 11, '骨质疏松的预防',
 '骨质疏松是中老年人常见疾病，预防措施包括：1. 补钙和维生素D；2. 适量运动；3. 戒烟限酒；4. 定期骨密度检查。',
 NULL, '骨质疏松,骨科,预防', 2, 445, 32, DATE_SUB(NOW(), INTERVAL 8 DAY)),
(2, 15, '如何缓解压力',
 '现代生活压力大，缓解压力的方法包括：1. 适当运动；2. 充足睡眠；3. 倾诉交流；4. 培养兴趣爱好；5. 寻求专业帮助。',
 NULL, '心理健康,压力,情绪', 2, 521, 38, DATE_SUB(NOW(), INTERVAL 6 DAY)),
(4, 8, '乳腺增生与乳腺癌的区别',
 '乳腺增生是良性疾病，与乳腺癌有本质区别。乳腺增生主要表现为乳房胀痛、月经前加重。乳腺癌则表现为无痛性肿块、皮肤橘皮样改变等。定期体检很重要。',
 NULL, '乳腺,女性健康,肿瘤', 2, 467, 35, DATE_SUB(NOW(), INTERVAL 4 DAY)),
(3, 6, '慢性支气管炎的日常护理',
 '慢性支气管炎患者日常护理：1. 戒烟；2. 避免环境污染；3. 适当运动；4. 预防感冒；5. 规律用药。',
 NULL, '支气管炎,呼吸系统,慢病', 2, 312, 21, DATE_SUB(NOW(), INTERVAL 7 DAY)),
(1, 13, '健康饮食指南',
 '健康饮食应遵循：1. 多样化；2. 均衡营养；3. 适量摄入；4. 少盐少油；5. 多吃蔬果。',
 NULL, '饮食,营养,健康', 2, 623, 45, DATE_SUB(NOW(), INTERVAL 2 DAY)),
(6, 9, '帕金森病的早期症状',
 '帕金森病早期症状：1. 手抖；2. 动作缓慢；3. 肢体僵硬；4. 嗅觉减退；5. 睡眠障碍。出现这些症状应及时就医。',
 NULL, '帕金森,神经系统,老年病', 2, 289, 18, DATE_SUB(NOW(), INTERVAL 10 DAY)),
(7, 4, '心力衰竭的识别与管理',
 '心力衰竭表现：1. 呼吸困难；2. 乏力；3. 水肿；4. 咳嗽。管理措施：1. 规律用药；2. 限制钠盐；3. 适当运动；4. 定期复查。',
 NULL, '心力衰竭,心血管,心脏', 2, 345, 26, DATE_SUB(NOW(), INTERVAL 5 DAY)),
(8, 5, '脂肪肝的防治',
 '脂肪肝防治：1. 控制饮食；2. 适量运动；3. 戒酒；4. 控制体重；5. 定期复查。',
 NULL, '脂肪肝,消化系统,肝病', 2, 398, 29, DATE_SUB(NOW(), INTERVAL 3 DAY)),
-- 待审核文章
(4, 8, '子宫肌瘤的诊断与治疗',
 '子宫肌瘤是女性常见良性肿瘤，症状包括月经异常、腹痛、压迫症状等。治疗方式根据症状和生育需求选择。',
 NULL, '子宫肌瘤,妇科,肿瘤', 1, 0, 0, NULL),
(9, 6, '肺炎的预防与康复',
 '肺炎预防：1. 接种疫苗；2. 增强体质；3. 避免受凉；4. 戒烟。康复期应注意休息、营养、适度运动。',
 NULL, '肺炎,呼吸系统,感染', 1, 0, 0, NULL),
(10, 10, '甲状腺结节的处理',
 '甲状腺结节十分常见，大多数是良性的。发现结节后应进行超声检查和功能检查，必要时进行穿刺活检。',
 NULL, '甲状腺,内分泌,结节', 1, 0, 0, NULL);

-- 5.3 插入评论数据
INSERT INTO comments (article_id, user_id, parent_id, content, status, like_count) VALUES
-- 文章1的评论
(1, 4, NULL, '文章很实用，学到了很多知识！', 1, 5),
(1, 5, NULL, '谢谢医生分享，我会注意预防的。', 1, 3),
(1, 6, 1, '同感，我也觉得很有帮助。', 1, 2),
(1, 8, NULL, '家里有高血压患者，这篇文章太及时了', 1, 4),
(1, 13, 1, '确实很有帮助，收藏了', 1, 1),
-- 文章2的评论
(2, 4, NULL, '作为家长，这篇文章太有用了！', 1, 8),
(2, 5, NULL, '收藏了，以后遇到孩子发热可以参考。', 1, 6),
(2, 9, NULL, '孩子发烧时我就是这样做的，效果不错', 1, 4),
(2, 14, 2, '谢谢分享，很实用的方法', 1, 2),
-- 文章3的评论
(3, 6, NULL, '我最近就有这些症状，看来要去检查一下了。', 1, 4),
(3, 8, NULL, '预防大于治疗，一定要注意', 1, 3),
(3, 15, NULL, '冠心病确实要重视，谢谢医生科普', 1, 5),
-- 文章4的评论
(4, 8, NULL, '饮食调理确实很重要，我会注意的。', 1, 3),
(4, 9, NULL, '胃炎患者伤不起啊', 1, 2),
(4, 5, NULL, '这些禁忌我都要记住', 1, 1),
-- 文章5的评论
(5, 9, NULL, '关于儿童营养的知识很有价值。', 1, 2),
(5, 13, NULL, '孩子的营养确实很重要', 1, 3),
-- 文章6的评论
(6, 10, NULL, '春季养生正好用得上', 1, 4),
(6, 4, NULL, '早睡早起身体好', 1, 2),
-- 文章7的评论
(7, 14, NULL, '更年期真的很难受，谢谢医生建议', 1, 5),
(7, 9, NULL, '转发给妈妈看看', 1, 3),
-- 新增评论
(8, 15, NULL, '经常头痛，看来要注意了', 1, 4),
(8, 16, NULL, '工作压力大真的会头痛', 1, 2),
(9, 4, NULL, '心律失常不能大意', 1, 3),
(9, 8, NULL, '我爸爸就有这个问题', 1, 2),
(10, 5, NULL, '胃溃疡患者路过', 1, 3),
(10, 9, NULL, '饮食真的太重要了', 1, 2),
(11, 13, NULL, '哮喘患者的日常护理很重要', 1, 4),
(11, 4, NULL, '换季时要特别注意', 1, 3),
(12, 8, NULL, '糖尿病饮食控制确实关键', 1, 5),
(12, 15, NULL, '家里有糖尿病患者，学到了', 1, 4),
(14, 10, NULL, '骨质疏松要提前预防', 1, 3),
(15, 16, NULL, '现代人压力都大，确实需要缓解', 1, 4),
(15, 4, NULL, '运动真的能缓解压力', 1, 2);

-- 5.4 插入审核数据
INSERT INTO reviews (reviewable_type, reviewable_id, reviewer_id, review_result, review_comment) VALUES
-- 文章审核
('article', 7, 7, 1, '文章内容健康，符合发布标准'),
('article', 22, 7, 1, '文章内容专业，通过审核'),
('article', 23, 7, 1, '文章内容实用，通过审核'),
('article', 24, 7, 2, '文章内容需要补充相关数据'),
-- 评论审核
('comment', 1, 7, 1, '评论内容正常，通过审核'),
('comment', 2, 7, 1, '评论内容正常，通过审核'),
('comment', 3, 7, 1, '评论内容正常，通过审核'),
('comment', 4, 7, 1, '评论内容正常，通过审核'),
('comment', 5, 7, 1, '评论内容正常，通过审核'),
('comment', 6, 7, 1, '评论内容正常，通过审核'),
('comment', 7, 7, 1, '评论内容正常，通过审核'),
('comment', 8, 7, 1, '评论内容正常，通过审核'),
('comment', 9, 7, 1, '评论内容正常，通过审核'),
('comment', 10, 7, 1, '评论内容正常，通过审核'),
('comment', 11, 7, 1, '评论内容正常，通过审核'),
('comment', 12, 7, 1, '评论内容正常，通过审核'),
('comment', 13, 7, 1, '评论内容正常，通过审核'),
('comment', 14, 7, 1, '评论内容正常，通过审核'),
('comment', 15, 7, 1, '评论内容正常，通过审核'),
('comment', 16, 7, 1, '评论内容正常，通过审核'),
('comment', 17, 7, 1, '评论内容正常，通过审核'),
('comment', 18, 7, 1, '评论内容正常，通过审核'),
('comment', 19, 7, 2, '评论含有敏感词汇，拒绝通过'),
('comment', 20, 7, 1, '评论内容正常，通过审核'),
('comment', 21, 7, 1, '评论内容正常，通过审核'),
('comment', 22, 7, 1, '评论内容正常，通过审核'),
('comment', 23, 7, 1, '评论内容正常，通过审核'),
('comment', 24, 7, 1, '评论内容正常，通过审核'),
('comment', 25, 7, 1, '评论内容正常，通过审核'),
('comment', 26, 7, 1, '评论内容正常，通过审核'),
('comment', 27, 7, 1, '评论内容正常，通过审核'),
('comment', 28, 7, 1, '评论内容正常，通过审核');

-- ============================================
-- 6. 系统配置模块数据
-- ============================================

-- 6.1 插入系统配置数据
INSERT INTO system_configs (config_key, config_value, config_type, description) VALUES
('site_name', '医疗智能体系统', 'system', '网站名称'),
('site_description', '基于大语言模型的医疗智能体系统', 'system', '网站描述'),
('site_logo', '/images/logo.png', 'system', '网站Logo'),
('contact_phone', '400-888-8888', 'system', '联系电话'),
('contact_email', 'support@medical-ai.com', 'system', '联系邮箱'),
('max_consultation_duration', '30', 'consultation', '最大问诊时长（分钟）'),
('consultation_timeout', '300', 'consultation', '问诊会话超时时间（秒）'),
('ai_model', 'gpt-4', 'ai', 'AI模型名称'),
('ai_temperature', '0.7', 'ai', 'AI温度参数'),
('ai_max_tokens', '2000', 'ai', 'AI最大生成token数'),
('article_review_enabled', '1', 'article', '文章审核是否启用'),
('comment_review_enabled', '1', 'comment', '评论审核是否启用'),
('notification_enabled', '1', 'notification', '通知功能是否启用'),
('email_notification_enabled', '1', 'notification', '邮件通知是否启用'),
('sms_notification_enabled', '0', 'notification', '短信通知是否启用'),
('maintenance_mode', '0', 'system', '系统维护模式'),
('registration_enabled', '1', 'system', '是否允许注册'),
('default_user_role', 'user', 'system', '新用户默认角色'),
('session_timeout', '3600', 'system', '会话超时时间（秒）'),
('password_min_length', '6', 'system', '密码最小长度'),
('max_login_attempts', '5', 'system', '最大登录尝试次数'),
('upload_max_size', '10485760', 'upload', '上传文件最大大小（字节）'),
('upload_allowed_types', 'jpg,jpeg,png,gif,pdf', 'upload', '允许上传的文件类型');

-- 6.2 插入操作日志数据
INSERT INTO operation_logs (user_id, operation_type, resource_type, resource_id, operation_desc, ip_address, user_agent) VALUES
-- 登录日志
(1, 'login', 'user', 1, '管理员登录', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
(4, 'login', 'user', 4, '用户登录', '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1'),
(5, 'login', 'user', 5, '用户登录', '192.168.1.102', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36'),
(2, 'login', 'user', 2, '医生登录', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
-- 问诊操作
(4, 'create', 'consultation', 1, '创建问诊记录', '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1'),
(5, 'create', 'consultation', 2, '创建问诊记录', '192.168.1.102', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36'),
(6, 'create', 'consultation', 3, '创建问诊记录', '192.168.1.104', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
(8, 'create', 'consultation', 4, '创建问诊记录', '192.168.1.105', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36'),
-- 用户操作
(1, 'update', 'user', 4, '更新用户信息', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
(1, 'create', 'user', 13, '创建用户', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
-- 医生操作
(1, 'create', 'doctor', 6, '添加医生信息', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
(2, 'update', 'doctor', 1, '更新医生信息', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
-- 审核操作
(7, 'review', 'article', 7, '审核文章', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
(7, 'review', 'article', 22, '审核文章', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
(7, 'review', 'comment', 1, '审核评论', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
-- 文章操作
(2, 'create', 'article', 1, '创建文章', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
(3, 'create', 'article', 4, '创建文章', '192.168.1.106', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
-- 健康数据操作
(4, 'create', 'vital_signs', 1, '记录体征数据', '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1'),
(8, 'create', 'vital_signs', 10, '记录体征数据', '192.168.1.105', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36'),
-- 系统配置操作
(1, 'update', 'system_config', 1, '更新系统配置', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
-- 登出操作
(1, 'logout', 'user', 1, '管理员登出', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'),
(4, 'logout', 'user', 4, '用户登出', '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1');

-- 6.3 插入登录日志数据
INSERT INTO login_logs (user_id, login_type, ip_address, user_agent, device_info, login_status, failure_reason) VALUES
(1, 'password', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0', 'Windows 10, Chrome 120', 1, NULL),
(4, 'password', '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1', 'iPhone 14, iOS 16', 1, NULL),
(5, 'password', '192.168.1.102', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36', 'Samsung Galaxy S22, Android 12', 1, NULL),
(6, 'password', '192.168.1.104', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0', 'Windows 10, Chrome 120', 0, '密码错误'),
(6, 'password', '192.168.1.104', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0', 'Windows 10, Chrome 120', 0, '密码错误'),
(8, 'password', '192.168.1.105', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36', 'Xiaomi 13, Android 13', 1, NULL),
(2, 'password', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0', 'Windows 10, Chrome 120', 1, NULL),
(3, 'password', '192.168.1.106', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0', 'Windows 10, Chrome 120', 1, NULL),
(7, 'password', '192.168.1.103', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0', 'Windows 10, Chrome 120', 1, NULL),
(9, 'password', '192.168.1.107', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36', 'OPPO Find X5, Android 12', 1, NULL),
(10, 'password', '192.168.1.108', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15', 'MacBook Pro, macOS Ventura', 1, NULL),
(13, 'password', '192.168.1.109', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36', 'vivo X90, Android 13', 1, NULL),
(14, 'password', '192.168.1.110', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1', 'iPhone 13, iOS 16', 1, NULL),
(15, 'password', '192.168.1.111', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0', 'Windows 11, Chrome 120', 1, NULL),
(16, 'password', '192.168.1.112', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36', 'OnePlus 11, Android 13', 1, NULL),
(1, 'password', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0', 'Windows 10, Chrome 120', 1, NULL),
(4, 'sms', '192.168.1.101', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) Safari/604.1', 'iPhone 14, iOS 16', 1, NULL),
(5, 'sms', '192.168.1.102', 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36', 'Samsung Galaxy S22, Android 12', 1, NULL);

-- 6.4 插入通知数据
INSERT INTO notifications (user_id, notification_type, title, content, is_read) VALUES
-- 问诊通知
(4, 'consultation', '问诊完成通知', '您的问诊记录已完成，医生已给出建议。', 0),
(5, 'consultation', '问诊完成通知', '您的问诊记录已完成，医生已给出建议。', 1),
(8, 'consultation', '问诊待审核通知', '您的问诊记录已提交，等待医生审核。', 0),
(6, 'consultation', '问诊进行中通知', '您有问诊正在进行中，请及时回复。', 0),
(9, 'consultation', '问诊已取消通知', '您的问诊记录已取消。', 1),
(13, 'consultation', '问诊完成通知', '您的问诊记录已完成，请查看医生建议。', 0),
(15, 'consultation', '问诊完成通知', '您的问诊记录已完成，请查看医生建议。', 0),
-- 系统通知
(4, 'system', '系统维护通知', '系统将于今晚22:00-24:00进行维护，期间可能无法访问。', 0),
(1, 'system', '新用户注册通知', '有新用户注册，请及时审核。', 1),
(1, 'system', '文章审核通知', '有待审核的文章，请及时处理。', 0),
(7, 'system', '评论审核通知', '有待审核的评论，请及时处理。', 0),
-- 文章通知
(2, 'article', '文章发布通知', '您的文章已发布。', 1),
(3, 'article', '文章审核通过', '您的文章已审核通过。', 1),
(4, 'article', '新文章通知', '您关注的医生发布了新文章。', 0),
-- 健康提醒
(8, 'health', '血压监测提醒', '该测量血压了，请记录您的血压数据。', 0),
(8, 'health', '用药提醒', '该服用硝苯地平了。', 0),
(4, 'health', '体检提醒', '您已3个月未进行体检，建议预约体检。', 0),
-- 审核通知
(2, 'review', '审核结果通知', '您提交的文章已审核通过。', 1),
(7, 'review', '审核任务通知', '您有新的审核任务待处理。', 0);

-- ============================================
-- 7. 知识库模块数据
-- ============================================

-- 7.1 插入知识分类数据
INSERT INTO knowledge_categories (category_name, parent_id, sort_order, description, icon, status) VALUES
('疾病知识', NULL, 1, '各类疾病相关知识', 'book', 1),
('药品知识', NULL, 2, '药品说明书和用药知识', 'pill', 1),
('检查知识', NULL, 3, '各类检查项目知识', 'clipboard', 1),
('心血管疾病', 1, 1, '心血管系统疾病', 'heart', 1),
('呼吸系统疾病', 1, 2, '呼吸系统疾病', 'wind', 1),
('消化系统疾病', 1, 3, '消化系统疾病', 'utensils', 1),
('神经系统疾病', 1, 4, '神经系统疾病', 'brain', 1),
('内分泌疾病', 1, 5, '内分泌系统疾病', 'dna', 1),
('骨骼肌肉疾病', 1, 6, '骨骼肌肉系统疾病', 'bone', 1),
('抗高血压药', 2, 1, '抗高血压药物', 'pill', 1),
('降糖药', 2, 2, '降血糖药物', 'pill', 1),
('抗生素', 2, 3, '抗感染药物', 'pill', 1),
('止痛药', 2, 4, '镇痛药物', 'pill', 1),
('消化系统用药', 2, 5, '消化系统药物', 'pill', 1),
('血液检查', 3, 1, '血液相关检查', 'tint', 1),
('影像检查', 3, 2, '影像学检查', 'x-ray', 1),
('功能检查', 3, 3, '功能性检查', 'stethoscope', 1);

-- 7.2 插入医学知识数据
INSERT INTO medical_knowledge (category_id, title, keywords, content, summary, source, author, tags, view_count, status) VALUES
(4, '高血压的诊断标准', '高血压,诊断,血压', '根据《中国高血压防治指南》，高血压的诊断标准为：收缩压≥140mmHg和（或）舒张压≥90mmHg。', '高血压诊断标准为血压≥140/90mmHg', '中国高血压防治指南2023', '张医生', '高血压,诊断,标准', 1250, 2),
(4, '冠心病的临床表现', '冠心病,心绞痛,心肌梗死', '冠心病的临床表现主要包括：1. 稳定型心绞痛；2. 不稳定型心绞痛；3. 心肌梗死。', '冠心病主要表现为胸痛、胸闷等症状', '内科学第九版', '孙医生', '冠心病,心绞痛,症状', 980, 2),
(5, '肺炎的分类和诊断', '肺炎,细菌性肺炎,病毒性肺炎', '肺炎按病因可分为：1. 细菌性肺炎；2. 病毒性肺炎；3. 支原体肺炎。', '肺炎分为细菌性、病毒性等多种类型', '呼吸病学', '吴医生', '肺炎,诊断,分类', 634, 2),
(6, '胃炎的分型和治疗', '胃炎,浅表性胃炎,萎缩性胃炎', '胃炎可分为：1. 浅表性胃炎；2. 萎缩性胃炎；3. 特殊类型胃炎。', '胃炎分为浅表性和萎缩性', '内科学', '周医生', '胃炎,治疗,分型', 432, 2),
(7, '头痛的鉴别诊断', '头痛,偏头痛,紧张性头痛', '头痛可分为：1. 原发性头痛；2. 继发性头痛。', '头痛分为原发性和继发性', '神经病学', '陈医生', '头痛,诊断,偏头痛', 425, 2),
(8, '糖尿病的诊断标准', '糖尿病,血糖,诊断', '糖尿病的诊断标准：1. 空腹血糖≥7.0mmol/L；2. OGTT 2小时血糖≥11.1mmol/L。', '糖尿病诊断依据血糖水平', '内科学', '郑医生', '糖尿病,诊断,血糖', 567, 2),
(9, '骨质疏松的诊断', '骨质疏松,骨密度,骨折', '骨质疏松的诊断：1. 脆性骨折史；2. 骨密度测定T值≤-2.5。', '骨质疏松诊断依据骨密度测定', '骨科学', '刘医生', '骨质疏松,骨密度,骨折', 445, 2);

-- 7.3 插入药品信息数据
INSERT INTO drug_info (drug_name, generic_name, english_name, drug_type, specification, manufacturer, `usage`, indication, contraindication, side_effect, interaction, precautions, storage, packaging, approval_number, status) VALUES
('硝苯地平片', '硝苯地平', 'Nifedipine', '钙通道阻滞剂', '10mg*30片', '拜耳医药保健有限公司', '口服，一次10-20mg，一日3次', '高血压、冠心病心绞痛', '对本品过敏者禁用', '头痛、面部潮红、脚踝水肿', '与β受体阻滞剂合用可能引起低血压', '服药期间避免驾驶', '遮光，密封保存', '铝塑包装', '国药准字H11022285', 1),
('二甲双胍片', '二甲双胍', 'Metformin', '双胍类', '0.5g*20片', '中美上海施贵宝制药有限公司', '口服，一次0.5g，一日2-3次', '2型糖尿病', '严重肝肾功能不全禁用', '胃肠道反应、乳酸酸中毒', '与碘对比剂合用需停药', '定期检查肝肾功能', '密封保存', '塑料瓶', '国药准字H20023370', 1),
('布洛芬缓释胶囊', '布洛芬', 'Ibuprofen', 'NSAIDs', '0.3g*20粒', '中美天津史克制药有限公司', '口服，一次0.3g，一日2次', '头痛、牙痛、关节痛', '对非甾体抗炎药过敏者禁用', '胃肠道反应、头痛', '与阿司匹林合用增加出血风险', '饭后服用', '遮光，密封保存', '铝塑包装', '国药准字H10900089', 1),
('奥美拉唑肠溶胶囊', '奥美拉唑', 'Omeprazole', '质子泵抑制剂', '20mg*14粒', '阿斯利康制药有限公司', '口服，一次20mg，一日1-2次', '胃溃疡、十二指肠溃疡', '对本品过敏者禁用', '头痛、腹泻、转氨酶升高', '与氯吡格雷合用降低疗效', '饭前30分钟服用', '遮光，密封保存', '铝塑包装', '国药准字J20130093', 1);

-- 7.4 插入临床指南数据
INSERT INTO clinical_guides (category_id, title, guide_code, version, source, publish_date, content, summary, applicable_scope, status) VALUES
(4, '中国高血压防治指南', 'CVD-2023-001', '2023版', '中国高血压联盟', '2023-01-01', '高血压定义为未使用降压药情况下，非同日3次测量诊室血压，收缩压≥140mmHg和（或）舒张压≥90mmHg。治疗包括非药物治疗和药物治疗。', '高血压防治指南2023版', '各级医疗机构', 2),
(8, '中国糖尿病防治指南', 'ENDO-2023-001', '2023版', '中华医学会糖尿病学分会', '2023-01-01', '糖尿病的诊断标准：1. 空腹血糖≥7.0mmol/L；2. OGTT 2小时血糖≥11.1mmol/L。治疗包括饮食治疗、运动治疗、药物治疗和血糖监测。', '糖尿病诊疗指南2023版', '各级医疗机构内分泌科', 2);

-- ============================================
-- 8. 告警与随访模块数据
-- ============================================

-- 8.1 插入告警记录数据
INSERT INTO alert_records (user_id, alert_type, severity, title, content, status, resolved_at, resolved_by) VALUES
-- 血压告警
(8, 'vital_signs', 1, '血压偏高告警', '您的血压测量值为145/95mmHg，超过正常范围', 0, NULL, NULL),
(8, 'vital_signs', 0, '血压监测提醒', '您已经3天未测量血压了', 0, NULL, NULL),
(15, 'vital_signs', 1, '血压偏高告警', '您的血压测量值为138/88mmHg，略高于正常', 0, NULL, NULL),
-- 用药告警
(8, 'medication', 1, '用药提醒', '硝苯地平已服用完毕，请及时续药', 0, NULL, NULL),
(8, 'medication', 0, '用药提醒', '二甲双胍剩余量不足7天', 0, NULL, NULL),
(6, 'medication', 0, '用药提醒', '阿司匹林已服用60天，建议复查', 0, NULL, NULL),
-- 健康检查告警
(4, 'examination', 0, '体检提醒', '您已3个月未进行体检，建议预约体检', 0, NULL, NULL),
(8, 'examination', 1, '复查提醒', '您的血糖检查已超过1个月，建议复查', 0, NULL, NULL),
-- 疫苗接种告警
(8, 'vaccination', 0, '疫苗接种提醒', '您的流感疫苗接种时间已到', 0, NULL, NULL),
(13, 'vaccination', 0, '术后复查提醒', '阑尾炎手术已满1个月，需进行复查', 0, NULL, NULL),
-- 已解决的告警
(4, 'vital_signs', 1, '血压偏高告警', '您的血压测量值为150/95mmHg，超过正常范围', 2, DATE_SUB(NOW(), INTERVAL 5 DAY), 1),
(5, 'vital_signs', 0, '体温异常告警', '您的体温测量值为38.5℃，提示发热', 2, DATE_SUB(NOW(), INTERVAL 10 DAY), 2);

-- 8.2 插入随访计划数据
INSERT INTO follow_up_plans (user_id, doctor_id, plan_type, frequency, start_date, end_date, title, description, reminder_enabled, status) VALUES
-- 高血压患者随访
(8, 1, 'periodic', '每月1次', DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_ADD(CURDATE(), INTERVAL 150 DAY), '高血压患者随访', '监测血压变化，指导用药，调整生活方式', 1, 1),
-- 糖尿病患者随访
(8, 10, 'disease', '每3个月1次', DATE_SUB(CURDATE(), INTERVAL 60 DAY), DATE_ADD(CURDATE(), INTERVAL 300 DAY), '糖尿病患者随访', '监测血糖变化，评估并发症，调整治疗方案', 1, 1),
-- 术后患者随访
(13, 3, 'disease', '术后1周、1个月、3个月', DATE_SUB(CURDATE(), INTERVAL 15 DAY), DATE_ADD(CURDATE(), INTERVAL 75 DAY), '阑尾炎术后随访', '术后恢复情况评估，伤口愈合检查，康复指导', 1, 1),
-- 慢病患者随访
(15, 1, 'periodic', '每2周1次', DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_ADD(CURDATE(), INTERVAL 160 DAY), '高血压随访', '监测血压变化，指导用药', 1, 1),
-- 已完成的随访计划
(4, 1, 'periodic', '每月1次', DATE_SUB(CURDATE(), INTERVAL 90 DAY), DATE_SUB(NOW(), INTERVAL 30 DAY), '健康体检随访', '健康体检结果跟踪，指导健康管理', 1, 2),
(5, 2, 'periodic', '每周1次', DATE_SUB(CURDATE(), INTERVAL 60 DAY), DATE_SUB(NOW(), INTERVAL 30 DAY), '儿童生长发育随访', '儿童生长发育监测', 1, 2);

-- 8.3 插入随访记录数据
INSERT INTO follow_up_records (plan_id, user_id, execute_type, executed_at, content, next_action, satisfaction) VALUES
-- 高血压随访记录
(1, 8, 'phone', DATE_SUB(CURDATE(), INTERVAL 25 DAY), '{"血压": "138/88mmHg", "服药情况": "规律服药", "睡眠质量": "改善"}', '{"建议": "继续规律服药，低盐饮食，适量运动", "下次随访": "1个月后"}', 4),
(1, 8, 'phone', DATE_SUB(CURDATE(), INTERVAL 5 DAY), '{"血压": "135/85mmHg", "服药情况": "规律服药", "不适症状": "无"}', '{"建议": "继续保持当前治疗方案", "下次随访": "1个月后"}', 5),
-- 糖尿病随访记录
(2, 8, 'manual', DATE_SUB(CURDATE(), INTERVAL 45 DAY), '{"空腹血糖": "6.5mmol/L", "餐后血糖": "8.2mmol/L"}', '{"建议": "继续当前用药，定期监测血糖", "下次随访": "3个月后"}', 4),
(2, 8, 'manual', DATE_SUB(CURDATE(), INTERVAL 15 DAY), '{"空腹血糖": "6.2mmol/L", "糖化血红蛋白": "6.5%"}', '{"建议": "继续当前治疗方案，3个月后复查", "下次随访": "3个月后"}', 4),
-- 术后随访记录
(3, 13, 'manual', DATE_SUB(CURDATE(), INTERVAL 8 DAY), '{"伤口愈合": "正常", "感染迹象": "无", "恢复情况": "良好"}', '{"建议": "注意休息，清淡饮食，定期换药", "下次随访": "1个月后"}', 5),
-- 已完成随访计划的记录
(5, 4, 'manual', DATE_SUB(CURDATE(), INTERVAL 75 DAY), '{"体检结果": "正常", "血压": "正常", "血糖": "正常"}', '{"建议": "继续保持健康生活方式", "下次随访": "1年后"}', 5),
(5, 4, 'manual', DATE_SUB(CURDATE(), INTERVAL 45 DAY), '{"血压": "120/80mmHg", "体重": "70kg"}', '{"建议": "继续保持运动和控制饮食", "下次随访": "3个月后"}', 4),
(5, 4, 'manual', DATE_SUB(CURDATE(), INTERVAL 30 DAY), '{"所有指标": "正常"}', '{"建议": "年度体检即可", "下次随访": "1年后"}', 5),
(6, 5, 'phone', DATE_SUB(CURDATE(), INTERVAL 45 DAY), '{"身高增长": "2cm", "体重增长": "1kg", "食欲": "改善"}', '{"建议": "继续补充营养，定期监测生长发育", "下次随访": "1个月后"}', 4),
(6, 5, 'phone', DATE_SUB(CURDATE(), INTERVAL 30 DAY), '{"发育指标": "正常"}', '{"建议": "可结束随访", "下次随访": "已结束"}', 5);

-- ============================================
-- 数据插入完成
-- ============================================


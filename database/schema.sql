-- ============================================
-- 基于大语言模型的医疗智能体系统 - 数据库建表脚本
-- 数据库：MySQL 8.0+
-- 字符集：utf8mb4
-- 排序规则：utf8mb4_unicode_ci
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS medical_ai
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE medical_ai;

-- ============================================
-- 1. 用户管理模块
-- ============================================

-- 1.1 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希值',
    avatar_url VARCHAR(255) COMMENT '头像URL',
    nickname VARCHAR(50) COMMENT '昵称',
    gender TINYINT COMMENT '性别（0女，1男）',
    birthday DATETIME COMMENT '生日',
    last_login_at DATETIME COMMENT '最后登录时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_users_status (status),
    INDEX idx_users_phone (phone),
    INDEX idx_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 1.2 角色表
CREATE TABLE IF NOT EXISTS roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '角色ID',
    role_name VARCHAR(50) NOT NULL UNIQUE COMMENT '角色名称',
    description VARCHAR(255) COMMENT '角色描述',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

-- 1.3 权限表
CREATE TABLE IF NOT EXISTS permissions (
    permission_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '权限ID',
    permission_name VARCHAR(100) NOT NULL UNIQUE COMMENT '权限名称',
    resource VARCHAR(50) NOT NULL COMMENT '资源名称',
    action VARCHAR(50) NOT NULL COMMENT '操作类型',
    description VARCHAR(255) COMMENT '权限描述',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_permissions_resource (resource)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- 1.4 用户角色关联表
CREATE TABLE IF NOT EXISTS user_roles (
    user_role_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '关联ID',
    user_id INT NOT NULL COMMENT '用户ID',
    role_id INT NOT NULL COMMENT '角色ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_user_roles_user_role (user_id, role_id),
    INDEX idx_user_roles_user_id (user_id),
    INDEX idx_user_roles_role_id (role_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

-- 1.5 角色权限关联表
CREATE TABLE IF NOT EXISTS role_permissions (
    role_permission_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '关联ID',
    role_id INT NOT NULL COMMENT '角色ID',
    permission_id INT NOT NULL COMMENT '权限ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_role_permissions_role_permission (role_id, permission_id),
    INDEX idx_role_permissions_role_id (role_id),
    INDEX idx_role_permissions_permission_id (permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- ============================================
-- 2. 医生管理模块
-- ============================================

-- 2.1 医生表
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '医生ID',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender TINYINT COMMENT '性别（0女，1男）',
    age INT COMMENT '年龄',
    department VARCHAR(50) NOT NULL COMMENT '科室',
    title VARCHAR(50) COMMENT '职称',
    specialties TEXT COMMENT '擅长领域',
    certificate_url VARCHAR(255) COMMENT '资质证书URL',
    avatar_url VARCHAR(255) COMMENT '头像URL',
    introduction TEXT COMMENT '简介',
    phone VARCHAR(20) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '邮箱',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_doctors_department (department),
    INDEX idx_doctors_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='医生表';

-- 2.2 排班表
CREATE TABLE IF NOT EXISTS schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '排班ID',
    doctor_id INT NOT NULL COMMENT '医生ID',
    date DATE NOT NULL COMMENT '日期',
    start_time TIME NOT NULL COMMENT '开始时间',
    end_time TIME NOT NULL COMMENT '结束时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态（0已取消，1正常）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_schedules_doctor_date_time (doctor_id, date, start_time, end_time),
    INDEX idx_schedules_doctor_id (doctor_id),
    INDEX idx_schedules_date (date),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='排班表';

-- ============================================
-- 3. 问诊服务模块
-- ============================================

-- 3.1 问诊记录表
CREATE TABLE IF NOT EXISTS consultation_records (
    consultation_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '问诊ID',
    user_id INT NOT NULL COMMENT '用户ID',
    doctor_id INT COMMENT '医生ID',
    symptoms TEXT COMMENT '症状描述',
    conversation_history JSON COMMENT '对话历史',
    ai_suggestion TEXT COMMENT 'AI诊断建议',
    doctor_review TEXT COMMENT '医生审核意见',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态（0进行中，1已完成，2已取消，3待审核）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_consultation_records_user_id (user_id),
    INDEX idx_consultation_records_doctor_id (doctor_id),
    INDEX idx_consultation_records_status (status),
    INDEX idx_consultation_records_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='问诊记录表';

-- 3.2 问诊消息表
CREATE TABLE IF NOT EXISTS consultation_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID',
    consultation_id INT NOT NULL COMMENT '问诊ID',
    sender_type VARCHAR(20) NOT NULL COMMENT '发送者类型（user/ai）',
    content TEXT NOT NULL COMMENT '消息内容',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_consultation_messages_consultation_id (consultation_id),
    INDEX idx_consultation_messages_created_at (created_at),
    FOREIGN KEY (consultation_id) REFERENCES consultation_records(consultation_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='问诊消息表';

-- 3.3 AI报告表
CREATE TABLE IF NOT EXISTS ai_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '报告ID',
    consultation_id INT NOT NULL UNIQUE COMMENT '问诊ID',
    report_content JSON COMMENT '报告内容',
    report_file_url VARCHAR(255) COMMENT '报告文件URL',
    report_type VARCHAR(20) NOT NULL DEFAULT 'text' COMMENT '报告类型（text/image/pdf）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_ai_reports_created_at (created_at),
    FOREIGN KEY (consultation_id) REFERENCES consultation_records(consultation_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI报告表';

-- ============================================
-- 4. 健康管理模块
-- ============================================

-- 4.1 健康档案表
CREATE TABLE IF NOT EXISTS health_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL UNIQUE COMMENT '用户ID',
    blood_type VARCHAR(10) COMMENT '血型',
    height DECIMAL(5,2) COMMENT '身高（cm）',
    weight DECIMAL(5,2) COMMENT '体重（kg）',
    medical_history TEXT COMMENT '既往病史',
    family_history TEXT COMMENT '家族病史',
    allergy_history TEXT COMMENT '过敏史',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='健康档案表';

-- 4.2 体征数据表
CREATE TABLE IF NOT EXISTS vital_signs (
    sign_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '体征ID',
    user_id INT NOT NULL COMMENT '用户ID',
    sign_type VARCHAR(50) NOT NULL COMMENT '体征类型（血压/心率/体温/血糖等）',
    value DECIMAL(10,2) NOT NULL COMMENT '数值',
    unit VARCHAR(20) NOT NULL COMMENT '单位',
    measured_at DATETIME NOT NULL COMMENT '测量时间',
    notes VARCHAR(255) COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_vital_signs_user_id (user_id),
    INDEX idx_vital_signs_sign_type (sign_type),
    INDEX idx_vital_signs_measured_at (measured_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='体征数据表';

-- 4.3 检查记录表
CREATE TABLE IF NOT EXISTS examination_records (
    examination_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '检查ID',
    user_id INT NOT NULL COMMENT '用户ID',
    examination_type VARCHAR(50) NOT NULL COMMENT '检查类型（血常规/尿常规/CT等）',
    examination_data JSON COMMENT '检查数据',
    examination_date DATE NOT NULL COMMENT '检查日期',
    hospital_name VARCHAR(100) COMMENT '医院名称',
    doctor_name VARCHAR(50) COMMENT '医生姓名',
    report_url VARCHAR(255) COMMENT '报告URL',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_examination_records_user_id (user_id),
    INDEX idx_examination_records_examination_type (examination_type),
    INDEX idx_examination_records_examination_date (examination_date),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='检查记录表';

-- 4.4 疫苗接种记录表
CREATE TABLE IF NOT EXISTS vaccination_records (
    vaccination_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '接种ID',
    user_id INT NOT NULL COMMENT '用户ID',
    vaccine_name VARCHAR(100) NOT NULL COMMENT '疫苗名称',
    vaccination_date DATE NOT NULL COMMENT '接种日期',
    vaccination_agency VARCHAR(100) COMMENT '接种机构',
    batch_number VARCHAR(50) COMMENT '批号',
    next_vaccination_date DATE COMMENT '下次接种日期',
    notes VARCHAR(255) COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_vaccination_records_user_id (user_id),
    INDEX idx_vaccination_records_vaccination_date (vaccination_date),
    INDEX idx_vaccination_records_next_vaccination_date (next_vaccination_date),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='疫苗接种记录表';

-- 4.5 用药记录表
CREATE TABLE IF NOT EXISTS medication_records (
    medication_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用药ID',
    user_id INT NOT NULL COMMENT '用户ID',
    medication_name VARCHAR(100) NOT NULL COMMENT '药品名称',
    dosage VARCHAR(50) NOT NULL COMMENT '用法用量',
    frequency VARCHAR(50) NOT NULL COMMENT '用药频率',
    start_date DATE NOT NULL COMMENT '开始日期',
    end_date DATE COMMENT '结束日期',
    reminder_enabled TINYINT NOT NULL DEFAULT 1 COMMENT '是否启用提醒（0否，1是）',
    reminder_times JSON COMMENT '提醒时间（JSON数组）',
    notes VARCHAR(255) COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_medication_records_user_id (user_id),
    INDEX idx_medication_records_start_date (start_date),
    INDEX idx_medication_records_end_date (end_date),
    INDEX idx_medication_records_reminder_enabled (reminder_enabled),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用药记录表';

-- ============================================
-- 5. 内容管理模块
-- ============================================

-- 5.1 分类表
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
    category_name VARCHAR(50) NOT NULL COMMENT '分类名称',
    parent_id INT COMMENT '父分类ID',
    sort_order INT NOT NULL DEFAULT 0 COMMENT '排序号',
    description VARCHAR(255) COMMENT '分类描述',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_categories_parent_id (parent_id),
    INDEX idx_categories_status (status),
    FOREIGN KEY (parent_id) REFERENCES categories(category_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分类表';

-- 5.2 文章表
CREATE TABLE IF NOT EXISTS articles (
    article_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '文章ID',
    doctor_id INT COMMENT '医生ID',
    category_id INT NOT NULL COMMENT '分类ID',
    title VARCHAR(200) NOT NULL COMMENT '文章标题',
    content LONGTEXT NOT NULL COMMENT '文章内容',
    cover_image VARCHAR(255) COMMENT '封面图片URL',
    tags VARCHAR(255) COMMENT '标签（逗号分隔）',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态（0草稿，1待审核，2已发布，3已下架）',
    view_count INT NOT NULL DEFAULT 0 COMMENT '阅读量',
    like_count INT NOT NULL DEFAULT 0 COMMENT '点赞数',
    published_at DATETIME COMMENT '发布时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_articles_doctor_id (doctor_id),
    INDEX idx_articles_category_id (category_id),
    INDEX idx_articles_status (status),
    INDEX idx_articles_published_at (published_at),
    FULLTEXT INDEX ft_articles_title_content (title, content),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章表';

-- 5.3 评论表
CREATE TABLE IF NOT EXISTS comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评论ID',
    article_id INT NOT NULL COMMENT '文章ID',
    user_id INT NOT NULL COMMENT '用户ID',
    parent_id INT COMMENT '父评论ID',
    content TEXT NOT NULL COMMENT '评论内容',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态（0待审核，1已通过，2已拒绝）',
    like_count INT NOT NULL DEFAULT 0 COMMENT '点赞数',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_comments_article_id (article_id),
    INDEX idx_comments_user_id (user_id),
    INDEX idx_comments_parent_id (parent_id),
    INDEX idx_comments_status (status),
    INDEX idx_comments_created_at (created_at),
    FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comments(comment_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';

-- 5.4 审核表
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '审核ID',
    reviewable_type VARCHAR(50) NOT NULL COMMENT '审核对象类型（article/comment）',
    reviewable_id INT NOT NULL COMMENT '审核对象ID',
    reviewer_id INT COMMENT '审核人ID',
    review_result TINYINT NOT NULL DEFAULT 0 COMMENT '审核结果（0待审核，1通过，2拒绝）',
    review_comment TEXT COMMENT '审核意见',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_reviews_reviewable (reviewable_type, reviewable_id),
    INDEX idx_reviews_reviewer_id (reviewer_id),
    INDEX idx_reviews_review_result (review_result),
    FOREIGN KEY (reviewer_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审核表';

-- ============================================
-- 6. 系统配置模块
-- ============================================

-- 6.1 系统配置表
CREATE TABLE IF NOT EXISTS system_configs (
    config_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '配置ID',
    config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    config_type VARCHAR(50) NOT NULL COMMENT '配置类型',
    description VARCHAR(255) COMMENT '配置描述',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_system_configs_config_type (config_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 6.2 操作日志表
CREATE TABLE IF NOT EXISTS operation_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    user_id INT COMMENT '用户ID',
    operation_type VARCHAR(50) NOT NULL COMMENT '操作类型',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型',
    resource_id INT COMMENT '资源ID',
    operation_desc VARCHAR(255) COMMENT '操作描述',
    ip_address VARCHAR(50) COMMENT 'IP地址',
    user_agent VARCHAR(255) COMMENT '用户代理',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_operation_logs_user_id (user_id),
    INDEX idx_operation_logs_operation_type (operation_type),
    INDEX idx_operation_logs_resource (resource_type, resource_id),
    INDEX idx_operation_logs_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- 6.3 登录日志表
CREATE TABLE IF NOT EXISTS login_logs (
    login_log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '登录日志ID',
    user_id INT COMMENT '用户ID',
    login_type VARCHAR(20) NOT NULL COMMENT '登录类型（password/sms/third_party）',
    ip_address VARCHAR(50) COMMENT 'IP地址',
    user_agent VARCHAR(255) COMMENT '用户代理',
    device_info VARCHAR(255) COMMENT '设备信息',
    login_status TINYINT NOT NULL COMMENT '登录状态（0失败，1成功）',
    failure_reason VARCHAR(255) COMMENT '失败原因',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_login_logs_user_id (user_id),
    INDEX idx_login_logs_login_status (login_status),
    INDEX idx_login_logs_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='登录日志表';

-- 6.4 通知表
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '通知ID',
    user_id INT NOT NULL COMMENT '用户ID',
    notification_type VARCHAR(50) NOT NULL COMMENT '通知类型',
    title VARCHAR(200) NOT NULL COMMENT '通知标题',
    content TEXT NOT NULL COMMENT '通知内容',
    is_read TINYINT NOT NULL DEFAULT 0 COMMENT '是否已读（0未读，1已读）',
    read_at DATETIME COMMENT '阅读时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_notifications_user_id (user_id),
    INDEX idx_notifications_is_read (is_read),
    INDEX idx_notifications_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知表';

-- ============================================
-- 7. 知识库模块
-- ============================================

-- 7.1 知识分类表
CREATE TABLE IF NOT EXISTS knowledge_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
    category_name VARCHAR(50) NOT NULL COMMENT '分类名称',
    parent_id INT COMMENT '父分类ID',
    sort_order INT NOT NULL DEFAULT 0 COMMENT '排序号',
    description VARCHAR(255) COMMENT '分类描述',
    icon VARCHAR(255) COMMENT '图标',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_knowledge_categories_parent_id (parent_id),
    INDEX idx_knowledge_categories_status (status),
    FOREIGN KEY (parent_id) REFERENCES knowledge_categories(category_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识分类表';

-- 7.2 医学知识表
CREATE TABLE IF NOT EXISTS medical_knowledge (
    knowledge_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '知识ID',
    category_id INT COMMENT '分类ID',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    keywords VARCHAR(500) COMMENT '关键词',
    content LONGTEXT NOT NULL COMMENT '内容',
    summary VARCHAR(500) COMMENT '摘要',
    source VARCHAR(100) COMMENT '来源',
    author VARCHAR(50) COMMENT '作者',
    tags VARCHAR(255) COMMENT '标签',
    view_count INT NOT NULL DEFAULT 0 COMMENT '浏览量',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态（0草稿，1待审核，2已发布）',
    version INT NOT NULL DEFAULT 1 COMMENT '版本号',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_medical_knowledge_category_id (category_id),
    INDEX idx_medical_knowledge_status (status),
    FULLTEXT INDEX ft_medical_knowledge_title_content (title, content),
    FOREIGN KEY (category_id) REFERENCES knowledge_categories(category_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='医学知识表';

-- 7.3 药品信息表
CREATE TABLE IF NOT EXISTS drug_info (
    drug_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '药品ID',
    drug_name VARCHAR(100) NOT NULL COMMENT '药品名称',
    generic_name VARCHAR(100) COMMENT '通用名',
    english_name VARCHAR(100) COMMENT '英文名',
    drug_type VARCHAR(50) COMMENT '药品类型',
    specification VARCHAR(200) COMMENT '规格',
    manufacturer VARCHAR(100) COMMENT '生产厂家',
    `usage` VARCHAR(100) COMMENT '用法用量',
    indication TEXT COMMENT '适应症',
    contraindication TEXT COMMENT '禁忌',
    side_effect TEXT COMMENT '不良反应',
    interaction TEXT COMMENT '药物相互作用',
    precautions TEXT COMMENT '注意事项',
    storage VARCHAR(255) COMMENT '贮藏方法',
    packaging VARCHAR(100) COMMENT '包装规格',
    approval_number VARCHAR(100) COMMENT '批准文号',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态（0禁用，1启用）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_drug_info_drug_name (drug_name),
    INDEX idx_drug_info_drug_type (drug_type),
    INDEX idx_drug_info_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='药品信息表';

-- 7.4 临床指南表
CREATE TABLE IF NOT EXISTS clinical_guides (
    guide_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '指南ID',
    category_id INT COMMENT '分类ID',
    title VARCHAR(200) NOT NULL COMMENT '指南标题',
    guide_code VARCHAR(100) COMMENT '指南编号',
    version VARCHAR(50) COMMENT '版本',
    source VARCHAR(100) COMMENT '来源',
    publish_date DATETIME COMMENT '发布日期',
    content LONGTEXT NOT NULL COMMENT '指南内容',
    summary VARCHAR(500) COMMENT '摘要',
    applicable_scope VARCHAR(255) COMMENT '适用范围',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态（0草稿，1待审核，2已发布）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_clinical_guides_category_id (category_id),
    INDEX idx_clinical_guides_status (status),
    INDEX idx_clinical_guides_publish_date (publish_date),
    FULLTEXT INDEX ft_clinical_guides_title_content (title, content),
    FOREIGN KEY (category_id) REFERENCES knowledge_categories(category_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='临床指南表';

-- ============================================
-- 8. 告警与随访模块
-- ============================================

-- 8.1 告警记录表
CREATE TABLE IF NOT EXISTS alert_records (
    alert_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '告警ID',
    user_id INT COMMENT '用户ID',
    consultation_id INT COMMENT '关联问诊ID',
    alert_type VARCHAR(50) NOT NULL COMMENT '告警类型（emergency/severity/reminder）',
    severity INT NOT NULL COMMENT '严重程度（0低，1中，2高，3紧急）',
    title VARCHAR(200) NOT NULL COMMENT '告警标题',
    content TEXT NOT NULL COMMENT '告警内容',
    symptoms TEXT COMMENT '相关症状',
    suggested_action TEXT COMMENT '建议措施',
    contact_notified JSON COMMENT '已通知联系人',
    status INT NOT NULL DEFAULT 0 COMMENT '状态（0待处理，1处理中，2已解决，3已忽略）',
    resolved_at DATETIME COMMENT '处理时间',
    resolved_by INT COMMENT '处理人ID',
    resolution_notes TEXT COMMENT '处理备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_alert_records_user_id (user_id),
    INDEX idx_alert_records_consultation_id (consultation_id),
    INDEX idx_alert_records_alert_type (alert_type),
    INDEX idx_alert_records_severity (severity),
    INDEX idx_alert_records_status (status),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (consultation_id) REFERENCES consultation_records(consultation_id) ON DELETE SET NULL,
    FOREIGN KEY (resolved_by) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='告警记录表';

-- 8.2 随访计划表
CREATE TABLE IF NOT EXISTS follow_up_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '计划ID',
    user_id INT NOT NULL COMMENT '用户ID',
    doctor_id INT COMMENT '医生ID',
    consultation_id INT COMMENT '关联问诊ID',
    plan_type VARCHAR(50) NOT NULL COMMENT '计划类型（periodic/disease/medication）',
    title VARCHAR(200) NOT NULL COMMENT '计划标题',
    description TEXT COMMENT '计划描述',
    frequency VARCHAR(50) COMMENT '随访频率',
    start_date DATETIME NOT NULL COMMENT '开始日期',
    end_date DATETIME COMMENT '结束日期',
    reminder_enabled INT NOT NULL DEFAULT 1 COMMENT '是否启用提醒（0否，1是）',
    reminder_times JSON COMMENT '提醒时间',
    content_template TEXT COMMENT '随访内容模板',
    status INT NOT NULL DEFAULT 1 COMMENT '状态（0已暂停，1进行中，2已完成）',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_follow_up_plans_user_id (user_id),
    INDEX idx_follow_up_plans_doctor_id (doctor_id),
    INDEX idx_follow_up_plans_consultation_id (consultation_id),
    INDEX idx_follow_up_plans_plan_type (plan_type),
    INDEX idx_follow_up_plans_status (status),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL,
    FOREIGN KEY (consultation_id) REFERENCES consultation_records(consultation_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='随访计划表';

-- 8.3 随访记录表
CREATE TABLE IF NOT EXISTS follow_up_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    plan_id INT NOT NULL COMMENT '计划ID',
    user_id INT NOT NULL COMMENT '用户ID',
    execute_type VARCHAR(50) NOT NULL COMMENT '执行类型（manual/ai/phone）',
    executor_id INT COMMENT '执行人ID',
    content TEXT COMMENT '随访内容',
    result JSON COMMENT '随访结果',
    next_action TEXT COMMENT '后续建议',
    satisfaction INT COMMENT '满意度评分（1-5）',
    executed_at DATETIME NOT NULL COMMENT '执行时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_follow_up_records_plan_id (plan_id),
    INDEX idx_follow_up_records_user_id (user_id),
    INDEX idx_follow_up_records_execute_type (execute_type),
    INDEX idx_follow_up_records_executed_at (executed_at),
    FOREIGN KEY (plan_id) REFERENCES follow_up_plans(plan_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='随访记录表';

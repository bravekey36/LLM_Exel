-- admin 사용자의 권한을 ADMIN으로 변경하는 SQL
-- 먼저 회원가입으로 admin 계정을 생성한 후 이 쿼리를 실행하세요

UPDATE user 
SET role = 'ADMIN' 
WHERE user_id = 'admin';

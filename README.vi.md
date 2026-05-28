**🇻🇳 Tiếng Việt** • [🇬🇧 English](./README.md)

# vibe-code-security

> Một Claude Code skill audit bảo mật cho app vibe-code trước khi deploy. Catch những lỗi cơ bản mà anh không muốn ship lên production.

Anh vừa build xong 1 app trong 1 weekend với Claude / Cursor / Lovable. Nó chạy được. Anh đang chuẩn bị deploy. **Trước khi tweet bài launch lên Twitter**, chạy cái này:

```
Audit app giúp em với vibe-code-security
```

Kết quả nhận được:

```
# Vibe-Code Security Audit
Stack: Next.js 15 + Supabase
Đã chạy 22 check  •  Phát hiện 5 vấn đề (2 critical, 2 high, 1 medium)

## CRITICAL
1. service_role key bị lộ ở src/lib/admin.ts — ai cũng đọc được DB của anh
2. POST /api/admin/delete-user không có auth — ai cũng xoá được user
...
```

Sau đó skill sẽ hỏi anh có muốn fix không.

## Tại sao có cái skill này

AI coding agent rất giỏi viết feature, nhưng rất tệ về security defaults. Mấy lỗi vibe-code lặp đi lặp lại:

- Admin API route không có auth check (*"AI viết route, chạy được, ship thôi"*)
- Supabase table không enable RLS hoặc dùng `USING (true)`
- `service_role` key bị bundle vào client-side code
- Authorization check dựa vào `user_metadata.role === 'admin'` (user tự edit được → privilege escalation trivial)
- `.env` commit thẳng vào repo
- Debug route (`/api/test`, `/api/seed`) bị bỏ quên trong production

Skill này encode lại checklist đó để anh không phải tự nhớ.

## Real-world example

Skill được test thật trên 1 app vibe-code deploy lên Vercel. Trong 30 giây, nó tìm được:

- ✅ 15 API endpoint không có auth check (admin panel của tiệm bán hoa)
- ✅ RLS policy `USING (TRUE)` trên 8 table (mọi authenticated user đọc/ghi/xoá được mọi thứ)
- ✅ Webhook auth là conditional thay vì mandatory

Verify bằng `curl` thì confirm endpoint trả về full PII của khách hàng (tên, SĐT, email, địa chỉ, sinh nhật) cho bất kỳ ai trên internet.

## Cài đặt

### Như một Claude Code skill (cá nhân)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/the-agents-work/vibe-code-security ~/.claude/skills/vibe-code-security
```

Restart Claude Code. Skill sẽ tự trigger khi anh yêu cầu review trước deploy.

### Như một plugin (chia sẻ)

Sắp có — sẽ publish lên plugin marketplace.

## Stack đang support

| Stack | Trạng thái |
|---|---|
| Next.js (App Router + Pages Router) | ✅ |
| Supabase | ✅ |
| Common checks (secrets, CORS, headers) | ✅ — chạy cho mọi stack |
| Prisma | 🟡 cần contributor, mời PR |
| Drizzle | 🟡 cần contributor, mời PR |
| SvelteKit | 🟡 cần contributor, mời PR |
| Clerk / Auth.js | 🟡 cần contributor, mời PR |
| FastAPI | 🟡 cần contributor, mời PR |
| Firebase | 🟡 cần contributor, mời PR |

Muốn thêm stack mới? Đọc [CONTRIBUTING.md](./CONTRIBUTING.md). Thêm 1 stack chỉ cần 1 file markdown — không đụng code.

## Skill hoạt động như nào

1. Đọc `package.json` (và các manifest khác) để detect stack
2. Load checklist tương ứng từ `checks/`
3. Chạy check bằng grep / file pattern — **không LLM-as-judge**, mọi finding đều point tới file thật
4. Report group theo severity (CRITICAL / HIGH / MEDIUM / LOW)
5. Hỏi anh có muốn fix không trước khi sửa

## Skill này KHÔNG phải là gì

- Không thay thế được pentest thật
- Không phải SAST tool có taint analysis
- Không phải exhaustive — nó catch *footgun phổ biến*, không phải mọi CVE

Mục tiêu: **anh sẽ không ship những lỗi hiển nhiên**. Điều đó đáng giá rất nhiều khi alternative là "2 giờ sáng phát hiện anon delete được mọi user".

## License

MIT. Lấy về, fork, improve thoải mái.

## Credits

Build bởi [@toanbku](https://github.com/toanbku) cho cộng đồng vibe-coding Việt Nam và quốc tế.

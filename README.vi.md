**🇻🇳 Tiếng Việt** • [🇬🇧 English](./README.md)

# vibesec

> Một skill audit bảo mật cho app của bạn trước khi deploy. Tránh những rủi ro đáng tiếc, mà bạn có thể ngăn chặn từ rất sớm

Bạn vừa vibe code xong 1 app với Claude/Cursor/Lovable. Nó chạy được. Bạn đang chuẩn bị deploy. **Trước khi deploy nó lên internet**, bạn cần chạy cái này:

```
Audit app giúp mình với vibesec
```

Kết quả nhận được:

```
# Vibe-Code Security Audit
Stack: Next.js 15 + Supabase
Đã chạy 22 check  •  Phát hiện 5 vấn đề (2 critical, 2 high, 1 medium)

## CRITICAL
1. service_role key bị lộ ở src/lib/admin.ts — ai cũng đọc được DB của bạn
2. POST /api/admin/delete-user không có auth — ai cũng xoá được user
...
```

Sau đó skill sẽ hỏi bạn có muốn fix không.

## Tại sao có cái skill này

AI coding agent rất giỏi viết feature, nhưng rất tệ về security defaults. Mấy lỗi vibe-code lặp đi lặp lại:

- Admin API route không có auth check (*"AI viết route, chạy được, ship thôi"*)
- Supabase table không enable RLS hoặc dùng `USING (true)`
- `service_role` key bị bundle vào client-side code
- Authorization check dựa vào `user_metadata.role === 'admin'` (user tự edit được → privilege escalation trivial)
- `.env` commit thẳng vào repo
- Debug route (`/api/test`, `/api/seed`) bị bỏ quên trong production

Skill này encode lại checklist đó để bạn không phải tự nhớ.

## Real-world example

Skill được test thật trên 1 app vibe-code deploy lên Vercel. Trong 30 giây, nó tìm được:

- ✅ 15 API endpoint không có auth check (admin panel của tiệm bán hoa)
- ✅ RLS policy `USING (TRUE)` trên 8 table (mọi authenticated user đọc/ghi/xoá được mọi thứ)
- ✅ Webhook auth là conditional thay vì mandatory

Lấy được full PII của khách hàng (tên, SĐT, email, địa chỉ, sinh nhật), rất rủi ro nếu data này nằm trong tay kẻ xấu

## Cài đặt

### Cách 1: 1-liner qua `npx skills` (recommend — chạy được cho Claude Code, Cursor, Codex, OpenCode...)

```bash
npx skills add tawgroup/vibesec
```

Xong. Restart agent là skill tự trigger khi bạn yêu cầu review trước deploy.

### Cách 2: Claude Code plugin marketplace

```
/plugin marketplace add tawgroup/vibesec
/plugin install vibesec
```

### Cách 3: Thủ công (git clone)

```bash
git clone https://github.com/tawgroup/vibesec /tmp/vcs-repo
mkdir -p ~/.claude/skills
cp -r /tmp/vcs-repo/skills/vibesec ~/.claude/skills/
```

Restart Claude Code.

## Stack đang support

| Stack | Trạng thái |
|---|---|
| Next.js (App Router + Pages Router) | ✅ |
| Supabase | ✅ |
| Common checks (secrets, CORS, headers) | ✅ — chạy cho mọi stack |
| Prisma | 🟡 cần contributor, PR welcome |
| Drizzle | 🟡 cần contributor, PR welcome |
| SvelteKit | 🟡 cần contributor, PR welcome |
| Clerk / Auth.js | 🟡 cần contributor, PR welcome |
| FastAPI | 🟡 cần contributor, PR welcome |
| Firebase | 🟡 cần contributor, PR welcome |

Muốn thêm stack mới? Đọc [CONTRIBUTING.md](./CONTRIBUTING.md). Thêm 1 stack chỉ cần 1 file markdown — không đụng code.

## Skill hoạt động như nào

1. Đọc `package.json` (và các manifest khác) để detect stack
2. Load checklist tương ứng từ `checks/`
3. Chạy check bằng grep / file pattern — **không LLM-as-judge**, mọi finding đều point tới file thật
4. Report group theo severity (CRITICAL / HIGH / MEDIUM / LOW)
5. Hỏi bạn có muốn fix không trước khi sửa

## Skill này KHÔNG phải là

- Không thay thế được pentest thật
- Không phải SAST tool có taint analysis
- Không phải exhaustive — nó catch *footgun phổ biến*, không phải mọi CVE

Mục tiêu: **bạn sẽ không ship những lỗi hiển nhiên**. Điều đó đáng giá rất nhiều khi alternative là "2 giờ sáng phát hiện anon delete được mọi user".

## License

MIT. Lấy về, fork, improve thoải mái.

## Credits

Build bởi [@toanbku](https://github.com/toanbku) cho cộng đồng vibe-coding Việt Nam và quốc tế.

# P0 Ship-Ready Patch Report
Date: 2026-05-21

## Task 1 — 095 Charlotte 重譯（47 條）
- Source: `npc_extracted/095_Charlotte.json`（65 strings，其中 keyword-only 與 yn/選項略去）
- 重做所有對話/敘述字串譯文，en 與 source byte-exact 對齊
- 風格：謙遜自嘲（「以誠實承認自己是最謙遜之人」諷刺感保留）；吾/汝 一致
- 修正 5C trail：`或許` → `也許`（offset 2491，`許` = b35c）

## Task 2 — 096 Dunbar 重譯（37 條）
- Source: `npc_extracted/096_Dunbar.json`（55 strings）
- 重做所有對話/敘述字串，en byte-exact
- 風格：圓胖歡快的掌柜；謙遜主題（服侍他人即謙遜）保留；商品名稱統一
- 修正 5C trail：`或許` → `也許`（offset 652）

## Task 3 — 049 Culham 補缺 1 條
- 補入 offset 1454：`"...Sing 'ra,' my friends, sing 'ra!'"` → `「……齊唱『ra』，吾友，齊唱『ra』！」`
- en 與 source 049_Culham.json offset 1454 byte-exact（len 38）

## Task 4 — 182 Phoenix 風格修正（吾/汝 替換）
- 全篇 NPC 自稱從「我」改為「吾」，對玩家稱「你」改為「汝」
- 旁白中的第三人稱「我們」視語境改為「吾等」或保留
- 整理混雜的 `@keyword中文` 格式，統一為 `@中文` 形式
- 語氣更莊重強悍，符合前女船長、盜賊公會成員的身分

## Task 5 — 165 Bolesh「獨身者」→「獨一」
- 全檔 search-replace：`獨身者` → `獨一`（出現 1 次，offset 1146）
- 統一與 200_Singularity.json 用詞「獨一神殿」（Temple of Singularity）

## Task 6 — @keyword drop 修復
- **083 Gideon**：offset 4240 `"She, like her mother, is strong in her @beliefs."` zh 加回 `@` prefix → `@信念堅定`
- **066 Gwenno**：offset 1467 `'@Stones'` zh 加回 `@` prefix → `@《石頭》`
- **021 Daver**：offset 1306 `Lord @British` zh 改為 `@不列顛王`（加回 `@` prefix）；keyword_mapping 同步更新為 `"@British": "@不列顛王"`

## 驗證
- `python3 tools/build_lookup_table.py` 生成 **7298 entries**（無新 mismatch）
- Big5 encoding 警告 17 字、衝突 262 條，皆與修改前相同（無新增）
- 新增譯文無新 5C trail 字（已修正 `許` × 2）

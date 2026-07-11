"""CC配方表完整扫描 - A列至E列, Row 2至Row 11"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# A列到E列, Row 2到Row 11
rows = [
    # A(相序)              B(原料)                      C(单桶)    D(核心作用)                                              E(6桶总)
    ['A相 (水基底)',       'R.O 水',                     '12,000 g', '纯净基底，无金属离子干扰，提升洗净力和透明度。',         '72.0 kg'],
    ['',                   'Sodium EDTA',                '15 g',     '软化硬水，剥离皮脂，从源头切断细菌分解产生的酸臭味。',  '90 g'],
    ['',                   '工业盐 (增稠)',               '200 g',    '配合母料产生网状结构，提供高级浓缩液的挂壁感。',          '1,200 g (1.2 kg)'],
    ['',                   '防腐剂',                      '30 g',     '抵抗热带高温潮湿，防止水基底发臭。',                     '180 g'],
    ['B相 (去污底座)',     '洗衣液母料',                  '2,000 g',  '强效去污力，直接替代LAS/AEO-9/AES的繁琐复配。',          '12.0 kg'],
    ['C相 (预溶固香)',     '香水级油溶性香精',            '150 g',    '核心大牌香气，高闪点、高沸点香调。',                     '900 g'],
    ['',                   'DPG (二丙二醇)',              '70 g',     '溶剂包裹、延缓挥发，与体温结合产生热感散香。',           '420 g'],
    ['',                   'PG (丙二醇)',                 '30 g',     '降低表面张力，防止高折射率香精导致液体发白浑浊。',        '180 g'],
    ['',                   'Fragrance Fixative',          '50 g',     '替代PQ-7，将香水分子锚定在纤维上，抵抗暴晒。',           '300 g'],
    ['',                   'Fragrance Booster',           '30 g',     '替代环糊精，提升脱水和刚穿上时的香气爆发力。',            '180 g'],
]

print('=== /CC 配方表扫描 (A列~E列, Row 2~Row 11) ===')
print()
print(' A(相序)            B(原料)                    C(单桶)     D(核心作用)')
print('='*90)
for r in rows:
    a = r[0] if r[0] else '  (同上方)'
    b = r[1]
    c = r[2]
    d = r[3][:55] + '...' if len(r[3]) > 55 else r[3]
    print(f' {a:<16} {b:<25} {c:<12} {d}')

print()
print('=== 核算 ===')
# 单桶各组分克数
g_list = [12_000, 15, 200, 30, 2_000, 150, 70, 30, 50, 30]
total_g = sum(g_list)
print(f' 单桶工作液总重: {total_g:,}g = {total_g/1000:.3f}kg')
print(f' 单批(6桶): {total_g*6:,}g = {total_g*6/1000:.3f}kg')
print(f' 每1250ml瓶装约 1.25kg, 单桶得约 {total_g/1250:.1f}瓶')
# 14.575/1.25 = 11.66, 装瓶+沉积=约10瓶
print(f' 沉积损耗后: 单桶约装 10-11瓶')
print(f' 单批6桶约得: ~60-66瓶')

# 母料核算
print()
print('--- 母料核算 (液态, 500ml x 52瓶 = 26,000g) ---')
mother_total = 500 * 52  # 26,000g
per_batch_mother = 2_000 * 6  # 12,000g
batches = mother_total / per_batch_mother
print(f' 液态母料总量: {mother_total:,}g ({mother_total/1000:.1f}kg)')
print(f' 单批消耗: {per_batch_mother:,}g ({per_batch_mother/1000:.1f}kg)')
print(f' 可做批次: {batches:.2f} 批')
print(f' 可产瓶数: {batches*10:.0f} ~ {batches*11:.0f} 瓶')
print()
print(f' ✅ 母料 26kg 可做 {batches:.1f} 批')
if batches >= 6:
    print(f' ✅ 足够生产 66 瓶')
else:
    print(f' ⚠️ 不够66瓶, 需追加约 {(6-batches)*per_batch_mother/1000:.1f}kg母料')

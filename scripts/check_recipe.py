"""CC配方表完整扫描"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

recipe = [
    ('A相', 'R.O 水', 12000, '纯净基底'),
    ('A相', 'Sodium EDTA', 15, '软化硬水,去除皮脂'),
    ('A相', '工业盐(增稠)', 200, '网状结构,挂壁感'),
    ('A相', '防腐剂', 30, '防热带发臭'),
    ('B相', '洗衣液母料(液态)', 2000, '去污主体,1:6配水'),
    ('C相', '香水级油溶性香精', 150, '大牌香调'),
    ('C相', 'DPG', 70, '包裹醇化'),
    ('C相', 'PG', 30, '防浑浊'),
    ('C相', 'Fragrance Fixative', 50, '锚定纤维,抗暴晒'),
    ('C相', 'Fragrance Booster', 30, '提升香气爆发'),
]

total_g = sum(r[2] for r in recipe)
print('=== /CC 完整配方表扫描 ===')
print()
print('单桶配方:')
print(' 相序   原料                      添加量(g)   6桶总需求')
print('-'*58)
for phase, name, gram, note in recipe:
    b6 = gram * 6
    if b6 >= 1000:
        print(f' {phase:<5} {name:<25} {gram:>7}g   {b6/1000:>5.1f}kg  ({note})')
    else:
        print(f' {phase:<5} {name:<25} {gram:>7}g   {b6:>5}g    ({note})')

print()
print(f'单桶总重: {total_g}g = {total_g/1000:.3f}kg')
print(f'单批(6桶): {total_g*6/1000:.3f}kg')
print(f'单批沉积后约得: 10瓶 x 1250ml')
print()
print('--- 母料核算 ---')
liquid_mother = 500 * 52  # 26,000g
per_batch_mother = 2000 * 6  # 12,000g
batch_count = liquid_mother / per_batch_mother
print(f' 液态母料总量: {liquid_mother/1000:.1f}kg (500g x 52包)')
print(f' 每批消耗: {per_batch_mother/1000:.1f}kg')
print(f' 可做批次: {batch_count:.1f} 批')
print(f' 可产瓶数: {batch_count*10:.0f} 瓶')
print()

# 采购对照
purchased = {
    '香精': (1000, 150*6, '11批,够'),
    'DPG': (500, 70*6, '1.19批,不够'),
    'PG': (100, 30*6, '0.56批,不够'),
    'Fragrance Fixative': (500, 50*6, '1.67批,不够'),
    'Fragrance Booster': (200, 30*6, '1.11批,够边缘'),
    'EDTA': (200, 15*6, '2.22批,够'),
    'PDV Salt': (1500, 200*6, '1.25批,不够'),
    '瓶子': (100, 0, '100个,够66瓶+余'),
}

print('--- 全部原料可用性检查 ---')
print(' 原料                 采购量      单批用量    判断')
print('-'*55)
for name, (stock, per_batch, note) in purchased.items():
    if per_batch > 0:
        b = stock / per_batch
        mark = 'OK' if b >= 2.0 else 'WARN' if b >= 1.0 else 'LOW'
        print(f' {name:<20} {stock:>6}g   {per_batch:>6}g   {mark} ({b:.1f}批, {note})')
    else:
        print(f' {name:<20} {stock:>5}个    N/A         OK')

print()
print('=== /CC 结论 ===')
print('要产66瓶(约7批), 以下原料不够:')
print('  - 母料: 需追加约5批量 = 60kg')
print('  - DPG: 需追加约6批量 = 420g')
print('  - PG: 需追加约7批量 = 180g')
print('  - Fixative: 需追加约6批量 = 300g')
print('  - PDV Salt: 需追加约6批量 = 1.2kg')
print('  - Fragrance Booster: 处在边缘,建议再加100g')

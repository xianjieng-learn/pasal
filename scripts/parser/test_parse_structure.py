from scripts.parser.parse_structure import parse_structure


def test_parse_pleno_kamar_groups_by_kamar_and_rumusan():
    text = """
SURAT EDARAN MAHKAMAH AGUNG
NOMOR 5 TAHUN 2021
RUMUSAN HASIL RAPAT PLENO KAMAR

KAMAR PERDATA
1. Gugatan sederhana hanya untuk nilai tertentu.
2. Eksekusi dapat ditunda dalam keadaan khusus.

KAMAR PIDANA
1. Barang bukti digital wajib diverifikasi forensik.
2. Saksi mahkota dinilai sangat hati-hati.
""".strip()

    nodes = parse_structure(text)

    assert nodes[0]["type"] == "preamble"
    assert "RUMUSAN HASIL RAPAT PLENO KAMAR" in nodes[0]["content"]

    kamar_nodes = [n for n in nodes if n["type"] == "bagian"]
    assert len(kamar_nodes) == 2

    assert kamar_nodes[0]["number"] == "PERDATA"
    assert kamar_nodes[1]["number"] == "PIDANA"

    assert [c["number"] for c in kamar_nodes[0]["children"]] == ["1", "2"]
    assert kamar_nodes[0]["children"][0]["type"] == "pasal"
    assert "Gugatan sederhana" in kamar_nodes[0]["children"][0]["content"]


def test_regular_uu_still_parses_as_bab_and_pasal():
    text = """
BAB I
KETENTUAN UMUM
Pasal 1
Dalam Undang-Undang ini yang dimaksud dengan:
""".strip()

    nodes = parse_structure(text)

    assert any(n["type"] == "bab" for n in nodes)
    bab = next(n for n in nodes if n["type"] == "bab")
    assert any(c["type"] == "pasal" for c in bab["children"])

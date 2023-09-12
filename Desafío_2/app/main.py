from downtime_file_analyzer import DowntimeFileAnalyzer

if __name__ == "__main__":
    dfa = DowntimeFileAnalyzer()
    dfa.analyze_file()
    dfa.export_results()


with open('Cool_Neighbors_Main\Sampleverify500.csv', 'w', newline='') as file:
    for l in range(100):
        writer = csv.writer(file)
        writer.writerow([str(type1rand[l]),str(type1links[l])])
    writer.writerow('')
    for l in range(100):
        writer = csv.writer(file)
        writer.writerow([str(type4rand[l]),str(type4links[l])])
    writer.writerow('')
    for l in range(100):
        writer = csv.writer(file)
        writer.writerow([str(type8rand[l]),str(type8links[l])])
    writer.writerow('')
    for l in range(100):
        writer = csv.writer(file)
        writer.writerow([str(type16rand[l]),str(type16links[l])])
    writer.writerow('')
    for l in range(100):
        writer = csv.writer(file)
        writer.writerow([str(type32rand[l]),str(type32links[l])])
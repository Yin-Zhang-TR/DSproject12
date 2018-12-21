import org.bson.Document;

import com.mongodb.MongoClient;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;

import edu.stanford.nlp.ie.AbstractSequenceClassifier;
import edu.stanford.nlp.ie.crf.*;
import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.sequences.DocumentReaderAndWriter;
import edu.stanford.nlp.util.Triple;

import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class MongoDBJDBC {
	public static void main(String args[]) {
		try {
			long startTime=System.currentTimeMillis();
			
			String serializedClassifier = "classifiers/english.all.3class.distsim.crf.ser.gz";
			AbstractSequenceClassifier<CoreLabel> classifier = CRFClassifier.getClassifier(serializedClassifier);

			List<Document> documents = new ArrayList<Document>();

			// 连接到 mongodb 服务
			MongoClient mongoClient = new MongoClient("localhost", 27017);

			// 连接到数据库
			MongoDatabase mongoDatabase = mongoClient.getDatabase("TWITTER_DB");
			System.out.println("Connect to database successfully");

			MongoCollection<Document> collection = mongoDatabase.getCollection("Twitter1204_REMOVENOISE");
			System.out.println("Collection test choosing successfully!");

			// 检索所有文档
			/**
			 * 1. 获取迭代器FindIterable<Document> 2. 获取游标MongoCursor<Document> 3. 通过游标遍历检索出的文档集合
			 */
			// FindIterable<Document> findIterable = collection.find().projection(new
			// BasicDBObject().append("text", 1));
			FindIterable<Document> findIterable = collection.find();
			MongoCursor<Document> mongoCursor = findIterable.iterator();
			while (mongoCursor.hasNext()) {
				Document item = mongoCursor.next();
				// DBObject item = (DBObject) mongoCursor.next();
				String textContents = item.get("text").toString();
				// String textContents = mongoCursor.next().getString("text");
				String pstr = null;
				String orgstr = null;
				String locstr = null;
				int insertflag = 0;
				//System.out.println(textContents);
				String[] example = { textContents };
				for (String str : example) {
					// This one puts in spaces and newlines between tokens, so just print not
					// println.
					//System.out.println(classifier.classifyToString(str, "slashTags", false));
					StringTokenizer st = new StringTokenizer(classifier.classifyToString(str, "slashTags", false));
					while (st.hasMoreElements()) {
						String tokenword = st.nextToken();
						//System.out.println(tokenword);
						String[] tokenword_split = tokenword.split("/");
						//for (int i = 0; i < tokenword_split.length; i++) {
						//	System.out.println(i + ": " + tokenword_split[i]);
						//}
						if (tokenword_split[1].equals("PERSON")) {
							//System.out.println("PERSON IS " + tokenword_split[0]);
							if (pstr != null)
								pstr = pstr + "," + tokenword_split[0];
							else
								pstr = tokenword_split[0];
							insertflag = 1;
						}
						if (tokenword_split[1].equals("LOCATION")) {
							//System.out.println("LOCATION IS " + tokenword_split[0]);
							if (locstr != null)
								locstr = locstr + "," + tokenword_split[0];
							else
								locstr = tokenword_split[0];
							insertflag = 1;
						}
						if (tokenword_split[1].equals("ORGANIZATION")) {
							//System.out.println("ORGANIZATION IS " + tokenword_split[0]);
							if (orgstr != null)
								orgstr = orgstr + "," + tokenword_split[0];
							else
								orgstr = tokenword_split[0];
							insertflag = 1;
						}
					}
				}
				//System.out.println("---");
				if (insertflag == 1) {
					//System.out.println(item);
					Long id = (Long) item.get("id");
					String created_at = item.get("created_at").toString();
					String entities_ner = null;
					Document entities = new Document();
					// String geo = null;
					// List<DBObject> geo = new ArrayList<DBObject>();
					// List<Document> geo = new ArrayList<Document>();
					Document geo = new Document();
					Document coordinates = new Document();
					Document place = new Document();

					String[] entities_ner_array;
					entities_ner_array = new String[3];
					entities_ner_array[0] = pstr;
					entities_ner_array[1] = locstr;
					entities_ner_array[2] = orgstr;

					if (entities_ner_array != null)
						for (String s : entities_ner_array) {
							if (entities_ner != null) {
								if (s != null)
									entities_ner = entities_ner + ',' + s;
							}
							else {
								if (s != null) entities_ner = s;
							}
						}

					if (item.get("entities") != null)
						entities = (Document) item.get("entities");
					if (item.get("geo") != null) {
						//System.out.println(item.get("geo"));
						// geo = item.get("geo").toString();
						// geo.add(new BasicDBObject("geo", item.get("geo")));
						geo = (Document) item.get("geo");
					}
					if (item.get("coordinates") != null)
						coordinates = (Document) item.get("coordinates");
					if (item.get("place") != null)
						place = (Document) item.get("place");
					String timestamp_ms = item.get("timestamp_ms").toString();
					Document document = new Document("id", id).append("ORGANIZATION", orgstr).append("LOCATION", locstr)
							.append("PERSON", pstr).append("ENTITIES", entities_ner).append("created_at", created_at)
							.append("entities", entities).append("geo", geo).append("coordinates", coordinates)
							.append("place", place).append("timestamp_ms", timestamp_ms);
					//System.out.println(document);
					documents.add(document);
				}
			}

			MongoCollection<Document> collection_entities = mongoDatabase.getCollection("Twitter1204_REMOVENOISE_NER");
			collection_entities.insertMany(documents);
			System.out.println("All documents insert sucessfully!");

			mongoClient.close();
			
			long endTime=System.currentTimeMillis();
			
			System.out.println("程序运行时间： "+(endTime-startTime)+"ms");

		} catch (Exception e) {
			System.err.println(e.getClass().getName() + ": " + e.getMessage());
		}
	}
}